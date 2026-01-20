FROM python:3.11-slim

RUN apt-get update && apt-get install -y build-essential python3-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY deploy-requirements.txt . 

RUN pip install --no-cache-dir -r deploy-requirements.txt 

RUN mkdir -p quantized deploy
COPY quantized/model-q8_0.gguf ./quantized/
COPY deploy/ ./deploy/

CMD ["uvicorn", "deploy.app:app", "--host", "0.0.0.0", "--port", "8000"]