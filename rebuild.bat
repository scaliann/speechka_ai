@echo off
echo 🔧 Полная пересборка Speechka Project...

REM Останавливаем и удаляем все контейнеры
echo 🛑 Остановка контейнеров...
docker-compose down

REM Удаляем все образы
echo 🗑️ Удаление образов...
docker-compose down --rmi all

REM Очищаем кэш Docker
echo 🧹 Очистка кэша...
docker system prune -f

REM Пересобираем
echo 🔨 Пересборка...
docker-compose up --build

echo ✅ Пересборка завершена!
pause
