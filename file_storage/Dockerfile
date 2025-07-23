FROM python:3.11-slim

ENV STORAGE_PATH=/usr/src/app/storage

WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app
COPY .env .

RUN mkdir -p $STORAGE_PATH

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
