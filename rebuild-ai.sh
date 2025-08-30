#!/bin/bash

echo "🔧 Пересборка AI Predict Service..."

# Останавливаем AI сервис
echo "🛑 Остановка AI сервиса..."
docker-compose stop ai_predict_service

# Удаляем образ AI сервиса
echo "🗑️ Удаление образа AI сервиса..."
docker-compose down --rmi ai_predict_service

# Очищаем кэш Docker для AI сервиса
echo "🧹 Очистка кэша..."
docker system prune -f

# Пересобираем только AI сервис
echo "🔨 Пересборка AI сервиса..."
docker-compose build --no-cache ai_predict_service

# Запускаем все сервисы
echo "🚀 Запуск всех сервисов..."
docker-compose up

echo "✅ Пересборка AI сервиса завершена!"
