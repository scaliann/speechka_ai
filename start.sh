#!/bin/bash

echo "🚀 Запуск Speechka Project..."

# Проверяем наличие .env файла
if [ ! -f "tg_bot_service/.env" ]; then
    echo "❌ Файл tg_bot_service/.env не найден!"
    echo "📝 Создайте файл tg_bot_service/.env на основе tg_bot_service/env.example"
    echo "🔑 Добавьте ваш Telegram Bot Token в BOT_TOKEN"
    exit 1
fi

# Проверяем, что BOT_TOKEN не пустой
if grep -q "BOT_TOKEN=your_bot_token_here" tg_bot_service/.env; then
    echo "❌ Не забудьте заменить BOT_TOKEN на реальный токен в tg_bot_service/.env"
    exit 1
fi

echo "✅ Конфигурация проверена"
echo "🐳 Запуск Docker Compose..."

# Останавливаем существующие контейнеры
docker-compose down

# Собираем и запускаем
docker-compose up --build

echo "🎉 Проект запущен!"
echo "📱 TG Bot готов к работе"
echo "🤖 AI Service доступен на http://localhost:8000"
