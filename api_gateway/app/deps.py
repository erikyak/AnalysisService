import httpx
from .config import TIMEOUT

client = httpx.AsyncClient(timeout=httpx.Timeout(TIMEOUT))

async def get_http_client() -> httpx.AsyncClient:
    return client
