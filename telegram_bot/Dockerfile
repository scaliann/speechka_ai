FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg \
 && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=2.1 POETRY_NO_INTERACTION=1 PIP_NO_CACHE_DIR=1 PYTHONUNBUFFERED=1
RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false \
 && poetry install --no-root --only main

COPY . .

ENV PYTHONPATH=/app

CMD ["python", "app/main.py"]