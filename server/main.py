from fastapi import FastAPI
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from contextlib import asynccontextmanager

import os

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
mongo_client = MongoClient(MONGODB_URL)
# db = os.getenv("DATABASE_NAME", "IntellegentImage")
database = mongo_client.get_database("sample_mflix")

app = FastAPI()

@asynccontextmanager
async def lifespan():
    # Startup logic
    print("Connecting to MongoDB...")
    # You can add more startup logic here if needed
    print("Connected to MongoDB.")
    yield
    # Shutdown logic can be added here if needed
    print("Closing MongoDB connection...")
    mongo_client.close()
    print("MongoDB connection closed.")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/movies")
def get_movies():
    movies_collection = database.get_collection("movies")
    movies = list(movies_collection.find().limit(10))  # Limit to 10 movies for brevity
    for movie in movies:
        movie["_id"] = str(movie["_id"])  # Convert ObjectId to string for JSON serialization
    return movies
