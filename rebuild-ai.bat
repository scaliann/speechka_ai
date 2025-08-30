@echo off
echo 🔧 Пересборка AI Predict Service...

REM Останавливаем AI сервис
echo 🛑 Остановка AI сервиса...
docker-compose stop ai_predict_service

REM Удаляем образ AI сервиса
echo 🗑️ Удаление образа AI сервиса...
docker-compose down --rmi ai_predict_service

REM Очищаем кэш Docker для AI сервиса
echo 🧹 Очистка кэша...
docker system prune -f

REM Пересобираем только AI сервис
echo 🔨 Пересборка AI сервиса...
docker-compose build --no-cache ai_predict_service

REM Запускаем все сервисы
echo 🚀 Запуск всех сервисов...
docker-compose up

echo ✅ Пересборка AI сервиса завершена!
pause
