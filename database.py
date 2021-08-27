from pymongo import MongoClient
from config import Config


class Database:
    def __init__(self, credentials, collection):
        if Config.username:
            self.client = MongoClient('mongodb://%s:%s@%s:%s' % (credentials['user'], credentials['password'],
                                                                 credentials['ip'], credentials['port']))
        else:
            self.client = MongoClient(credentials['ip'], credentials['port'])

        self.db = self.client[credentials['db_name']]
        self.collection = self.db[collection]

    def delete(self, query):
        return self.collection.delete_one(query)

    def update(self, query, new_values):
        return self.collection.update_one(query, new_values)

    def find_one(self, query):
        return self.collection.find_one(query)

    def find(self, query=None):
        to_return = []

        found = self.collection.find(query)
        for item in found:
            to_return.append(item)

        return to_return

    def insert(self, query):
        self.collection.insert_one(query)
