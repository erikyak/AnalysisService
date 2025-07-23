from sqlalchemy.orm import Session
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
from . import crud, schemas, models
from .db import SessionLocal, engine
from .utils import compute_hash, save_file_to_disk


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="File Storing Service", version="1.0")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/files/", response_model=schemas.FileResponse)
async def upload_file(
    uploaded_file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    file_hash = compute_hash(uploaded_file)

    existing = crud.get_file_by_hash(db, file_hash)
    if existing:
        return {"file_id": existing.id}

    path = save_file_to_disk(uploaded_file, file_hash)

    file_in = schemas.FileCreate(
        name=uploaded_file.filename, hash=file_hash, location=path
    )
    db_obj = crud.create_file(db, file_in)

    return {"file_id": db_obj.id}

@app.get("/files/{file_id}")
def download_file(file_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(models.File).filter(models.File.id == file_id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="File not found")

    file_path: str = str(db_obj.location)
    file_name: str = str(db_obj.name)

    return FileResponse(
        path=file_path,
        media_type="application/octet-stream",
        filename=file_name,
    )
