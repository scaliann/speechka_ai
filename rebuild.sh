#!/bin/bash

echo "🔧 Полная пересборка Speechka Project..."

# Останавливаем и удаляем все контейнеры
echo "🛑 Остановка контейнеров..."
docker-compose down

# Удаляем все образы
echo "🗑️ Удаление образов..."
docker-compose down --rmi all

# Очищаем кэш Docker
echo "🧹 Очистка кэша..."
docker system prune -f

# Пересобираем
echo "🔨 Пересборка..."
docker-compose up --build

echo "✅ Пересборка завершена!"
