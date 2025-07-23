from pydantic import BaseModel

class FileCreate(BaseModel):
    name: str
    hash: str
    location: str

class FileResponse(BaseModel):
    file_id: int

    class Config:
        orm_mode = True
