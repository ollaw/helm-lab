
from ast import pattern
import logging
import json
import os
from datetime import datetime
from flask import Flask, render_template, request, abort
from flask_cors import CORS
from logging.handlers import TimedRotatingFileHandler
from flasgger import Swagger, swag_from
from utils import get_host_ip
from data_manager import DataManager

app = Flask(__name__)

#region Logger
"""
LOG_FILE_NAME = os.path.join(
    APP_ROOT,
    'logs',
    'mvcapp',
    'mvcapp.log')

logging.basicConfig(filename=LOG_FILE_NAME,
    level=logging.DEBUG,
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

handler = TimedRotatingFileHandler(LOG_FILE_NAME, when="midnight", interval=1)
handler.suffix = "%Y%m%d"
app.logger.addHandler(handler)
"""

logging.basicConfig(level=logging.DEBUG)
#endregion

#region CORS
CORS(app)
#endregion

#region SWAGGER

try:

    from flasgger import Swagger, swag_from

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "version": "1.0.0",
            "title": "Web Library Open API",
            "description": "Web Library Application API Specification",
            "contact": {
                "responsibleOrganization": "Depo",
                "responsibleDeveloper": "Depo",
                "email": "teo@maculade.com",
                "url": "www.maculade.com"
            },
            "license": {
                "name": "MIT",
                "url": "https://opensource.org/licenses/MIT"
            }
        },
        "tags": [
            {
                "name": "Utils",
                "description": "Tools and Utils API"
            }
        ],
        "schemes": ["http"],
        "consumes": ["application/json"],
        "produces": ["application/json"]
    }

    swag = Swagger(app, template=swagger_template)

except:
    def swag_from(*args, **kwargs):
        pass

#endregion

#region Globals
VERSION = "2.0.0"
#endregion

try:
    data_manager = DataManager(host=os.environ["REDIS_HOST"], port=os.environ["REDIS_PORT"], db=os.environ["REDIS_DB"], password=os.environ["REDIS_PASS"])
except Exception as exc:
    app.logger.error(f"Exception {type(exc)} - Cannot connect to Redis - {exc}")

#region Routes
@app.route('/')
def index():
    return render_template("index.html", host_ip=get_host_ip())

@app.route("/search")
def search():
    return render_template("search.html", host_ip=get_host_ip())

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == 'POST':

        book_api = {}
        book_api['title'] = request.form.get("title_p")
        book_api['author'] = request.form.get("author_p")
        book_api['year'] = request.form.get("year_p")
        book_api['isbn'] = request.form.get("isbn_p")

        if data_manager.save(book_isbn=book_api['isbn'], book_data=json.dumps(book_api)):
            return render_template("message.html", message=f"Book {book_api['isbn']} added!", host_ip=get_host_ip() )
        else:
            abort(500)

    else:

        return render_template("single_book.html", action="add", host_ip=get_host_ip())

@app.route("/search_result", methods=["GET","POST"])
def search_result():
    search_p = request.form.get("search_p")
    books = data_manager.load_all(pattern=search_p)
    return render_template("books.html", books=books, host_ip=get_host_ip())

@app.route("/book/<string:book_isbn>", methods=["GET"])
def search_single_book(book_isbn):

    book=data_manager.load(book_isbn)
    return render_template("single_book.html", book=book, isbn=book_isbn, host_ip=get_host_ip() )

@app.route("/book/<string:book_isbn>", methods=["DELETE"])
def delete_single_book(book_isbn):

    if data_manager.delete(book_isbn):
        return render_template("message.html", message=f"Book ISBN: {book_isbn} deleted!", host_ip=get_host_ip() )
    else:
        return render_template("message.html", error=True, message=f"Errors deleting book ISBN: {book_isbn}!", host_ip=get_host_ip() )


@app.route("/books")
def books():
    books = data_manager.load_all()
    return render_template("books.html", books=books, host_ip=get_host_ip())


@app.route('/healthcheck', methods=['GET'])
@swag_from('swagger/healthcheck.yaml')
def api_barcode():
    response = {
        "result": "OK",
        "reason": "Healthcheck"
    }

    return response

#endregion

#region APIs

@app.route("/api/books", methods=["GET"])
@swag_from('swagger/get_all_books.yaml')
def get_all_books_api():

    try:
        return data_manager.load_all()
    except NameError as exc:
        app.logger.error(f"Exception {type(exc)} - Cannot load books - {exc}")
        abort(500)
    except Exception as exc:
        app.logger.error(f"Exception {type(exc)} - Cannot load books - {exc}")
        abort(404)


@app.route("/api/<string:book_isbn>", methods=["GET"])
@swag_from('swagger/get_book.yaml')
def get_book_api(book_isbn):

    try:
        return data_manager.load(book_isbn)
    except NameError as exc:
        app.logger.error(f"Exception {type(exc)} - Cannot load book - {exc}")
        abort(500)
    except Exception as exc:
        app.logger.error(f"Exception {type(exc)} - Cannot load book - {exc}")
        abort(404)


@app.route("/api/<string:book_isbn>", methods=["POST"])
@swag_from('swagger/set_book.yaml')
def set_book_api(book_isbn):

    try:
        content = request.get_json()

        book_api = {}

        book_api['title'] = content.get('title')
        book_api['author'] = content.get('author')
        book_api['year'] = content.get('year')
        book_api['isbn'] = book_isbn

        sysconf = {}
        sysconf['host'] = get_host_ip()

        response = {}
        response['book'] = book_api
        response['sysconf'] = sysconf

        if data_manager.save(book_isbn=book_isbn, book_data=json.dumps(book_api)):
            return response, 201
        else:
            abort(500)

    except Exception as exc:
        app.logger.error(f"Exception {type(exc)} - Cannot save book - {exc}")
        abort(500)
    

@app.route("/api/<string:book_isbn>", methods=["DELETE"])
@swag_from('swagger/delete_book.yaml')
def delete_book_api(book_isbn):

    try:
        if data_manager.delete(book_isbn):
            return f"{book_isbn} deleted", 200
        else:
            raise Exception()
    except NameError as exc:
        app.logger.error(f"Exception {type(exc)} - Cannot delete book - {exc}")
        abort(500)
    except Exception as exc:
        app.logger.error(f"Exception {type(exc)} - Cannot delete book, not found")
        abort(404)

#endregion