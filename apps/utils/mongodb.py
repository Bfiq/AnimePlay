from pymongo import MongoClient
from decouple import config

def get_mongo_client():
    connection_string = config('MONGO_CONNECTION')
    client = MongoClient(connection_string)
    return client

def get_database():
    client = get_mongo_client()
    return client[config('MONGO_DATABASE')]

def close_connection(client):
    client.close()
