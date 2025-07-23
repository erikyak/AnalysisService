import os
from dotenv import load_dotenv

load_dotenv()

FILE_STORAGE_URL  = os.getenv("FILE_STORAGE_URL")
FILE_ANALYSIS_URL = os.getenv("FILE_ANALYSIS_URL")
TIMEOUT           = float(os.getenv("HTTP_TIMEOUT", "10.0"))
FILE_ANALYSIS_IMAGE_URL = os.getenv("FILE_ANALYSIS_IMAGE_URL")
