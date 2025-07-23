from pydantic import BaseModel, Field
from typing import Dict

class AnalysisResult(BaseModel):
    file_id: int
    paragraph_count: int
    word_count: int
    char_count: int
    frequencies: Dict[str, int]
    image_url: str

    class Config:
        from_attributes = True

class ImageResponse(BaseModel):
    file_id: int
    image_url: str

    class Config:
        from_attributes = True