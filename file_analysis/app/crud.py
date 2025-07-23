from sqlalchemy.orm import Session
from . import models, schemas


def get_analysis(db: Session, file_id: int):
    return db.query(models.Analysis).filter(models.Analysis.file_id == file_id).first()

def create_analysis(db: Session, result: schemas.AnalysisResult):
    db_obj = models.Analysis(
        file_id=result.file_id,
        paragraph_count=result.paragraph_count,
        word_count=result.word_count,
        char_count=result.char_count,
        frequencies=result.frequencies,
        image_location=result.image_url,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj