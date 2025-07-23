import os
from pathlib import Path
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import FileResponse
from .db import SessionLocal, engine
from . import models, schemas, crud, utils

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="File Analysis Service", version="1.0")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/analyze/{file_id}", response_model=schemas.AnalysisResult)
async def analyze(file_id: int, db: Session = Depends(get_db)):
    cached = crud.get_analysis(db, file_id)
    if cached:
        return schemas.AnalysisResult(
            file_id=cached.file_id,
            paragraph_count=cached.paragraph_count,
            word_count=cached.word_count,
            char_count=cached.char_count,
            frequencies=cached.frequencies,
            image_url=cached.image_location,
        )

    text = await utils.fetch_file_text(file_id)

    p_cnt, w_cnt, c_cnt, freqs = utils.analyze_text(text)

    image_path = await utils.generate_wordcloud(text, file_id)

    result = schemas.AnalysisResult(
        file_id=file_id,
        paragraph_count=p_cnt,
        word_count=w_cnt,
        char_count=c_cnt,
        frequencies=freqs,
        image_url=image_path,
    )
    crud.create_analysis(db, result)

    return result


@app.get(
    "/analyze/{file_id}",
    response_model=schemas.AnalysisResult,
)
def get_analysis(file_id: int, db: Session = Depends(get_db)):
    analysis = crud.get_analysis(db, file_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    return schemas.AnalysisResult(
        file_id=analysis.file_id,
        paragraph_count=analysis.paragraph_count,
        word_count=analysis.word_count,
        char_count=analysis.char_count,
        frequencies=analysis.frequencies,
        image_url=analysis.image_location
    )
@app.get("/analyze/{file_id}/image")
def get_wordcloud_image(file_id: int, db: Session = Depends(get_db)):
    from .config import STORAGE_PATH

    analysis = crud.get_analysis(db, file_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    filename = analysis.image_location
    full_path = Path(STORAGE_PATH) / filename

    actual = os.listdir(STORAGE_PATH)

    if not full_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Word cloud image not found: expected {filename}, actual files: {actual}"
        )

    return FileResponse(path=full_path, media_type="image/png", filename=None)