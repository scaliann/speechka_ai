FROM python:3.12-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    curl \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Копирование requirements и установка зависимостей
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY app/ ./app/



# Переменные окружения
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Открываем порт для FastAPI
EXPOSE 8000

# Команда запуска
CMD ["python", "app/main.py"]
