@echo off
echo 🚀 Запуск Speechka Project...

REM Проверяем наличие .env файла
if not exist "tg_bot_service\.env" (
    echo ❌ Файл tg_bot_service\.env не найден!
    echo 📝 Создайте файл tg_bot_service\.env на основе tg_bot_service\env.example
    echo 🔑 Добавьте ваш Telegram Bot Token в BOT_TOKEN
    pause
    exit /b 1
)

REM Проверяем, что BOT_TOKEN не пустой
findstr "BOT_TOKEN=your_bot_token_here" tg_bot_service\.env >nul
if %errorlevel% equ 0 (
    echo ❌ Не забудьте заменить BOT_TOKEN на реальный токен в tg_bot_service\.env
    pause
    exit /b 1
)

echo ✅ Конфигурация проверена
echo 🐳 Запуск Docker Compose...

REM Останавливаем существующие контейнеры
docker-compose down

REM Собираем и запускаем
docker-compose up --build

echo 🎉 Проект запущен!
echo 📱 TG Bot готов к работе
echo 🤖 AI Service доступен на http://localhost:8000
pause
