import os
import httpx
from pathlib import Path
from datetime import datetime
from collections import Counter
from fastapi import HTTPException
from .config import FILE_STORAGE_URL, WORDCLOUD_API_URL, STORAGE_PATH

async def fetch_file_text(file_id: int) -> str:
    url = f"{FILE_STORAGE_URL}/{file_id}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        if resp.status_code != 200:
            raise HTTPException(status_code=502, detail="File Storage Service error")
        return resp.text

def analyze_text(text: str):
    paragraphs = [p for p in text.split('\n\n') if p.strip()]
    paragraph_count = len(paragraphs)
    words = text.split()
    word_count = len(words)
    char_count = len(text)
    frequencies = Counter(words)
    return paragraph_count, word_count, char_count, dict(frequencies)

def top_words(frequencies: dict, top_n: int = 50) -> list[tuple[str, int]]:
    return Counter(frequencies).most_common(top_n)

async def generate_wordcloud(text: str, file_id: int) -> str:
    words = text.lower().split()
    freq = Counter(words)
    top = top_words(freq, top_n=50)

    text_value = ",".join(f"{word}:{count}" for word, count in top)

    payload = {
        "format": "png",
        "width": 1000,
        "height": 1000,
        "useWordList": True,
        "cleanWords": False,
        "text": text_value
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            WORDCLOUD_API_URL,
            json=payload,
            timeout=30.0
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=502, detail="Word Cloud API error")

        content = resp.content

    os.makedirs(STORAGE_PATH, exist_ok=True)
    timestamp = int(datetime.now().timestamp())
    filename = f"wordcloud_{file_id}_{timestamp}.png"
    save_path = Path(STORAGE_PATH) / filename
    save_path.write_bytes(content)

    return filename