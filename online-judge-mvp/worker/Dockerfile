FROM python:3.12-slim
WORKDIR /worker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY worker.py .
ENV REDIS_HOST=redis REDIS_PORT=6379
# Cần Docker CLI trong worker để spawn container judge:
RUN apt-get update && apt-get install -y --no-install-recommends docker.io && rm -rf /var/lib/apt/lists/*
# Worker chạy với Docker socket được mount từ compose (add below in compose if needed)
CMD ["python", "worker.py"]
RUN apt-get update && apt-get install -y --no-install-recommends docker.io && rm -rf /var/lib/apt/lists/*
