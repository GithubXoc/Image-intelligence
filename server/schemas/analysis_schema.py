from pydantic import BaseModel
class AnalysisSchema(BaseModel):
    file_uuid: str
    file_name: str
    image_url: str
    created_at: str # ISO formatted datetime string
    analysis_result: dict
