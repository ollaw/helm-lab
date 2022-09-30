import csv
import json
import os
from data_manager import DataManager

try:
    data_manager = DataManager(host=os.environ["REDIS_HOST"], port=os.environ["REDIS_PORT"], db=os.environ["REDIS_DB"], password=os.environ["REDIS_PASS"])
except Exception as exc:
    print(f"Exception {type(exc)} - Cannot connect to Redis - {exc}")


with open('books.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)

    for row in reader:
        book_data = {}
        book_data['title'] = row[1]
        book_data['author'] = row[2]
        book_data['year'] = row[3]
        book_data['isbn'] = row[0]
        data_manager.save(book_isbn=row[0], book_data=json.dumps(book_data))

    print("Import books from CSV file completed with success!")