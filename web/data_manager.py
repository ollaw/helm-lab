import json
import os
import redis

class DataManager:

    def __init__(self, host, port, db, password=None):
        self.redis = redis.StrictRedis(host, port, db, password)


    def save(self, book_isbn, book_data):
        return self.redis.set(book_isbn, book_data)


    def load(self, book_isbn):

        return json.loads(self.redis.get(book_isbn))


    def load_all(self, pattern=None):

        books = {}
        books_keys = []
        
        if pattern:
            books_keys = self.redis.keys(pattern=f"*{pattern}*")
        else:
            books_keys = self.redis.keys()

        for key in books_keys:
            books[key.decode()] = self.load(key)

        return books


    def delete(self, book_isbn):
        return self.redis.delete(book_isbn)
