from fastapi import APIRouter

router = APIRouter(prefix="/analyze-image")

@router.post("/")
async def analyze_image():
    return {"message": "Image analysis not yet implemented."}

@router.get("/{id}")
async def analysis_status(id: str):
    return {"analyze": f"Analysis data for id: {id}."}