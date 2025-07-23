from sqlalchemy import Column, Integer, String
from .db import Base

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    hash = Column(String, unique=True, index=True, nullable=False)
    location = Column(String, nullable=False)
