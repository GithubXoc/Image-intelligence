from fastapi import APIRouter, HTTPException, status
from server.db.mongo import MONGO_DB_COLLECTIONS, get_mongo_client
import pymongo

router = APIRouter(prefix="/history")

mongo_client = get_mongo_client()

@router.get("/")
async def get_history(limit: int = 20, skip: int = 0):
    try:
        result = []
        # Placeholder for fetching history from database
        history_data = mongo_client.get_collection(MONGO_DB_COLLECTIONS.IMAGE_ANALYSES).find().skip(skip).limit(limit).sort("created_at",pymongo.DESCENDING)
        for item in history_data:
            item["_id"] = str(item["_id"])
            result.append(item)
        return result
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
