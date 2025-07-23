import os
from dotenv import load_dotenv
load_dotenv()

DB_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/"
    f"{os.getenv('POSTGRES_DB')}"
)

FILE_STORAGE_URL = os.getenv('FILE_STORAGE_URL')
WORDCLOUD_API_URL = os.getenv('WORDCLOUD_API_URL')
STORAGE_PATH = os.getenv('STORAGE_PATH')