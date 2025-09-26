FROM python:3.12-slim

WORKDIR /app

# Системные пакеты (ffmpeg тебе нужен) + инструменты сборки
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg build-essential git \
    && rm -rf /var/lib/apt/lists/*

# Обновляем pip И ставим setuptools+wheel (важно!)
RUN python -m pip install --upgrade pip setuptools wheel && pip cache purge



COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

CMD ["python", "app/main.py"]