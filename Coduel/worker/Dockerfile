FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive

# Prepare Docker CLI (worker needs to call docker run for judge image)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    gnupg \
 && rm -rf /var/lib/apt/lists/*

RUN install -m 0755 -d /etc/apt/keyrings \
 && curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg \
 && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(. /etc/os-release && echo $VERSION_CODENAME) stable" > /etc/apt/sources.list.d/docker.list

RUN apt-get update && apt-get install -y --no-install-recommends docker-ce-cli && rm -rf /var/lib/apt/lists/*

ENV DEBIAN_FRONTEND=

WORKDIR /worker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY worker.py .
ENV REDIS_HOST=redis REDIS_PORT=6379
# Worker runs with Docker socket mounted from compose (add below in compose if needed)
CMD ["python", "worker.py"]
