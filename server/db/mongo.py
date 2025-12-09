
from functools import lru_cache
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from types import SimpleNamespace

import os

MONGODB_URL = os.getenv("MONGODB_URL")

MONGO_DB_COLLECTIONS = SimpleNamespace(
    IMAGE_ANALYSES="image_analyses",
    USER="user_collection"
)

class MongoDB:
    def __init__(self, connection_string: str = MONGODB_URL):
        self.client = MongoClient(connection_string)
        # self.users_collection = self.db['users']
        # self.images_collection = self.db['images']
        self.movies_db = self.client.get_database("sample_mflix")
        print(f"Connected to database: sample_mflix")
    
    def get_collection(self, collection_name: str):
        return self.movies_db.get_collection(collection_name)
    
    def write_collection(self, collection_name: str, data: dict):
        collection = self.movies_db.get_collection(collection_name)
        result = collection.insert_one(data)
        return result.inserted_id
    
    def close_connection(self):
        self.client.close()
        print("MongoDB connection closed.")
        
@lru_cache()
def get_mongo_client():
    return MongoDB()
