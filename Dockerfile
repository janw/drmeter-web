# syntax=docker/dockerfile:1
FROM python:3.11-slim

WORKDIR /
RUN --mount=type=bind,target=/src \
    set -e; \
    apt-get update -y; \
    apt-get install -y --no-install-recommends libsndfile1; \
    apt-get clean; \
    rm -rf /var/lib/apt/lists/*; \
    pip install --no-cache-dir /src

ENTRYPOINT [ "uvicorn", "drmeter_web:app" ]
CMD [ "--host", "0.0.0.0", "--port", "8000" ]

EXPOSE 8000
