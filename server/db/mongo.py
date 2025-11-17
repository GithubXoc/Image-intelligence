
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

uri = os.getenv("MONGODB_URL")

# Create a new client and connect to the server
client = MongoClient(uri)

class MongoDB:
    def __init__(self):
        self.db = client['IntellegentImage']
        self.users_collection = self.db['users']
        self.images_collection = self.db['images']
    
    def get_users_collection(self):
        return self.users_collection

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)