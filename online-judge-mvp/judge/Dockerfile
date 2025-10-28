FROM debian:12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc g++ time ca-certificates procps \
    python3 python3-venv python3-pip \
    nodejs \
    openjdk-17-jdk-headless \
    && rm -rf /var/lib/apt/lists/*

ENV LC_ALL=C TZ=UTC
WORKDIR /work

# user không đặc quyền
RUN useradd -m runner
USER runner

# copy script vào image
COPY --chown=runner:runner compile_run.sh /usr/local/bin/compile_run.sh
RUN chmod +x /usr/local/bin/compile_run.sh
COPY --chown=runner:runner run_with_metrics.py /usr/local/bin/run_with_metrics.py
RUN chmod +x /usr/local/bin/run_with_metrics.py

# seccomp profile sẽ được mount từ ngoài nếu cần (Docker Desktop có profile mặc định)
