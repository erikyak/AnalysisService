import hashlib
import os
from fastapi import UploadFile
from dotenv import load_dotenv

load_dotenv()
STORAGE_PATH = os.getenv("STORAGE_PATH")
HASH_ALGO = os.getenv("HASH_ALGO", "sha256")

def compute_hash(file: UploadFile) -> str:
    hasher = hashlib.new(HASH_ALGO)
    file.file.seek(0)
    for chunk in iter(lambda: file.file.read(8192), b""):
        hasher.update(chunk)
    file.file.seek(0)
    return hasher.hexdigest()

def save_file_to_disk(file: UploadFile, file_hash: str) -> str:
    ext = os.path.splitext(file.filename)[1]
    filename = f"{file_hash}{ext}"
    path = os.path.join(STORAGE_PATH, filename)
    with open(path, "wb") as buffer:
        buffer.write(file.file.read())
    return path
