FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Очистка pip кэша и обновление pip
RUN pip install --upgrade pip && pip cache purge

# Копирование requirements и установка зависимостей
COPY requirements.txt .
RUN cat requirements.txt && echo "Installing requirements..." && pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY src/ ./src/

# Создание директории для записей
RUN mkdir -p /app/records

# Переменные окружения
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Команда запуска
CMD ["python", "src/main.py"]
