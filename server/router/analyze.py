from fastapi import APIRouter, File, UploadFile, HTTPException, status

import os
import shutil
import logging

import uuid

from server.db.mongo import MONGO_DB_COLLECTIONS, get_mongo_client
from server.services.ai_service import gemini_analyze_image_ai
from server.services.storage import upload_file_to_s3

router = APIRouter(prefix="/analyze-image")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

mongo_client = get_mongo_client()

### TODO: Implement analyze image functionality
# Upload image
# Save temporarily
# Send to AI
# Detect objects in image
# Try product matching
# Save result to DB
# Return json response

@router.post("/")
async def analyze_image(file: UploadFile = File(...)):
    try:
        # Temp file saving logic
        file_uuid = str(uuid.uuid4())
        file_location = os.path.join("/tmp", f"{file_uuid}_{file.filename}")

        image_bytes = await file.read()

        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Analyze image using AI service
        try:
            ai_response = gemini_analyze_image_ai(image_bytes)
        except Exception as e:
            print(f"Error during AI analysis: {e}")
            ai_response = None
        is_analyzed = ai_response is not None
            
        # Upload to S3
        try:
            upload_file_to_s3(file_location, f"uploads/{file_uuid}_{file.filename}", file, is_analyzed)
        except Exception as e:
            print(f"Error uploading file to S3: {e}")
            logger.error(f"Error uploading file to S3: {e}")
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
        # Post analysis result to MongoDB (to be implemented)
        if is_analyzed:
            write_analysis_to_db({
                "file_uuid": file_uuid,
                "file_name": file.filename,
                "analysis_result": ai_response
            })

        return {"message": f"Successfully uploaded {file.filename}", "file_path": file_location}
    except Exception as e:
        raise e
    finally:
        file.file.close()

@router.get("/{id}")
async def analysis_status(id: str):
    return {"analyze": f"Analysis data for id: {id}."}

@router.get("/file-uuid/{file_uuid}")
async def get_analysis_by_file_uuid(file_uuid: str) -> dict:
    try:
        collection = mongo_client.get_collection(MONGO_DB_COLLECTIONS.IMAGE_ANALYSES)
        analysis = collection.find_one({"file_uuid": file_uuid})
        if not analysis:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Analysis not found")
        analysis["_id"] = str(analysis["_id"])
        return analysis

    except Exception as e:
        logger.error(f"Error fetching analysis from DB: {e}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



def write_analysis_to_db(analysis_data: dict):
    try:
        inserted_id = mongo_client.write_collection(MONGO_DB_COLLECTIONS.IMAGE_ANALYSES, analysis_data)
        return inserted_id
    except Exception as e:
        logger.error(f"Error writing analysis to DB: {e}")
        raise e