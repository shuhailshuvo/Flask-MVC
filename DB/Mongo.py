from pymongo import MongoClient


def connect(table):
    client = MongoClient('mongodb://localhost:27017')
    return client.pydb[table]
