from fastapi import FastAPI
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from server.db.mongo import get_mongo_client

from .router import analyze

load_dotenv()

app = FastAPI()

app.include_router(analyze.router)

mongo_client = get_mongo_client()

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
    movies_collection = mongo_client.get_collection("movies")
    movies = list(movies_collection.find().limit(10))
    for movie in movies:
        movie["_id"] = str(movie["_id"])
    return movies
