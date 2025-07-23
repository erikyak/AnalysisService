from sqlalchemy.orm import Session
from . import models, schemas

def get_file_by_hash(db: Session, hash_: str):
    return db.query(models.File).filter(models.File.hash == hash_).first()

def create_file(db: Session, file: schemas.FileCreate):
    db_obj = models.File(**file.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
