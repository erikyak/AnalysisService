from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.responses import JSONResponse, StreamingResponse, Response
import httpx
from .config import FILE_STORAGE_URL, FILE_ANALYSIS_URL
from .deps import get_http_client
from .deps import client

app = FastAPI(title="API Gateway", version="1.0")

@app.post("/files/")
async def upload_file(
    uploaded_file: UploadFile = File(...),
    client: httpx.AsyncClient = Depends(get_http_client)
):
    url = f"{FILE_STORAGE_URL}/"
    try:
        files = {
            "uploaded_file": (
                uploaded_file.filename,
                await uploaded_file.read(),
                uploaded_file.content_type
            )
        }
        resp = await client.post(url, files=files)
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"File Storage error: {e}")

    return JSONResponse(status_code=resp.status_code, content=resp.json())

@app.get("/files/{file_id}")
async def download_file(
    file_id: int,
    client: httpx.AsyncClient = Depends(get_http_client)
):
    url = f"{FILE_STORAGE_URL}/{file_id}"

    async def file_iterator():
        async with client.stream("GET", url) as upstream:
            if upstream.status_code != 200:
                content = await upstream.aread()
                raise HTTPException(
                    status_code=upstream.status_code,
                    detail=content.decode(errors="ignore")
                )
            async for chunk in upstream.aiter_bytes(chunk_size=64 * 1024):
                yield chunk

    return StreamingResponse(
        file_iterator(),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename=\"{file_id}\""}
    )

@app.post("/analyze/{file_id}")
async def analyze_file(file_id: int, client: httpx.AsyncClient = Depends(get_http_client)):
    url = f"{FILE_ANALYSIS_URL}/{file_id}"
    try:
        resp = await client.post(url)
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"File Analysis error: {e}")
    return JSONResponse(status_code=resp.status_code, content=resp.json())


@app.get("/analyze/{file_id}")
async def get_analysis(file_id: int, client: httpx.AsyncClient = Depends(get_http_client)):
    url = f"{FILE_ANALYSIS_URL}/{file_id}"
    resp = await client.get(url)
    if resp.status_code != 200:
        detail = None
        try:
            detail = resp.json()
        except:
            detail = resp.text
        raise HTTPException(status_code=resp.status_code, detail=detail)
    return JSONResponse(status_code=200, content=resp.json())

@app.get("/analyze/{file_id}/image")
async def proxy_wordcloud_image(
    file_id: int,
    client: httpx.AsyncClient = Depends(get_http_client)
):
    upstream_url = f"{FILE_ANALYSIS_URL}/{file_id}/image"
    async with client.stream("GET", upstream_url) as resp:
        if resp.status_code != 200:
            body = await resp.aread()
            raise HTTPException(status_code=resp.status_code, detail=body.decode(errors="ignore"))

        content = await resp.aread()
        return Response(content, media_type="image/png")