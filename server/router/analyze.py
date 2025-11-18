from fastapi import APIRouter, File, UploadFile
import os
import shutil

router = APIRouter(prefix="/analyze-image")

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
        file_location = os.path.join("/tmp", file.filename)

        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {"message": f"Successfully uploaded {file.filename}", "file_path": file_location}
    except Exception as e:
        return {"error": str(e)}
    finally:
        file.file.close()

@router.get("/{id}")
async def analysis_status(id: str):
    return {"analyze": f"Analysis data for id: {id}."}