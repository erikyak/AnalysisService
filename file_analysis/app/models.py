from sqlalchemy import Column, Integer, String, JSON
from .db import Base

class Analysis(Base):
    __tablename__ = 'analysis'
    file_id = Column(Integer, primary_key=True, index=True)
    paragraph_count = Column(Integer, nullable=False)
    word_count = Column(Integer, nullable=False)
    char_count = Column(Integer, nullable=False)
    frequencies = Column(JSON, nullable=False)
    image_location = Column(String, nullable=False)