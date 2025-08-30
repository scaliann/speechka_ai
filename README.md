# Speechka Project

Проект состоит из двух сервисов:
- **TG Bot Service** - Telegram бот для записи голоса и диагностики речи
- **AI Predict Service** - FastAPI сервис с нейронной сетью для анализа речи

## Быстрый запуск с Docker Compose

### 1. Подготовка

1. Скопируйте файл конфигурации:
```bash
# Linux/Mac
cp tg_bot_service/env.example tg_bot_service/.env

# Windows
copy tg_bot_service\env.example tg_bot_service\.env
```

2. Отредактируйте `tg_bot_service/.env` и добавьте ваш Telegram Bot Token:
```
BOT_TOKEN=your_actual_bot_token_here
DATABASE_URL=sqlite+aiosqlite:///./bot_database.db
```

**Как получить BOT_TOKEN:**
- Напишите @BotFather в Telegram
- Создайте нового бота командой `/newbot`
- Скопируйте полученный токен в файл `.env`

### 2. Запуск

**Автоматический запуск (рекомендуется):**
```bash
# Linux/Mac
./start.sh

# Windows
start.bat
```

**Ручной запуск:**
```bash
docker-compose up --build
```

**Запуск в фоновом режиме:**
```bash
docker-compose up -d --build
```

**Полная пересборка (если есть проблемы):**
```bash
# Linux/Mac
./rebuild.sh

# Windows
rebuild.bat
```

**Пересборка только AI сервиса:**
```bash
# Linux/Mac
./rebuild-ai.sh

# Windows
rebuild-ai.bat
```

### 3. Проверка работы

- **AI Predict Service** будет доступен на `http://localhost:8000`
- **TG Bot Service** запустится и будет готов к работе с Telegram

### 4. Остановка

```bash
docker-compose down
```

## Структура проекта

```
speechka_project/
├── ai_predict_service/     # AI сервис с нейронной сетью
├── tg_bot_service/         # Telegram бот
├── records/                # Общая папка для аудиофайлов
├── docker-compose.yml      # Конфигурация Docker Compose
└── README.md
```

## Архитектура

1. **TG Bot Service** записывает голосовые сообщения пользователей
2. Аудиофайлы сохраняются в папку `records/`
3. При запросе диагностики, TG Bot отправляет пути к файлам в AI Predict Service
4. AI Predict Service анализирует аудио и возвращает диагноз и рекомендации

## Переменные окружения

### TG Bot Service
- `BOT_TOKEN` - токен Telegram бота
- `DATABASE_URL` - URL базы данных SQLite

### AI Predict Service
- Автоматически настраивается для работы в Docker

## Проверка работы

### Проверка AI Predict Service
```bash
curl http://localhost:8000/health
```

### Проверка TG Bot
- Найдите вашего бота в Telegram
- Отправьте команду `/start`

## Логи

Просмотр логов:
```bash
# Все сервисы
docker-compose logs

# Конкретный сервис
docker-compose logs tg_bot_service
docker-compose logs ai_predict_service

# Логи в реальном времени
docker-compose logs -f
```

## Устранение неполадок

### Проблема: Бот не отвечает
1. Проверьте, что BOT_TOKEN правильный
2. Проверьте логи: `docker-compose logs tg_bot_service`

### Проблема: AI сервис не работает
1. Проверьте логи: `docker-compose logs ai_predict_service`
2. Проверьте доступность: `curl http://localhost:8000/health`

### Проблема: Ошибки с аудиофайлами
1. Убедитесь, что папка `records/` существует
2. Проверьте права доступа к папке

### Проблема: Ошибки установки зависимостей
1. Удалены Windows-специфичные пакеты (pywin32, wincertstore)
2. Обновлены версии пакетов для совместимости с Docker
3. Используется Python 3.8 для AI сервиса
4. Создан минимальный requirements файл без проблемных зависимостей

**Если ошибка с pywin32 все еще возникает:**
```bash
# Принудительная пересборка AI сервиса
./rebuild-ai.sh  # Linux/Mac
rebuild-ai.bat   # Windows
```

## Остановка и очистка

```bash
# Остановка сервисов
docker-compose down

# Остановка с удалением volumes
docker-compose down -v

# Полная очистка (удаление образов)
docker-compose down --rmi all
```
