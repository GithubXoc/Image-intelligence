from pydantic import BaseModel

class UploadedImageSchema(BaseModel):
    filename: str
    url: str