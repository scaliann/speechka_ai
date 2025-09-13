import asyncio
import logging


from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from config import settings
from db.db_helper import init_db
from handlers import (
    start_router,
    recording_router,
    menu_router,
    user_router,
)

load_dotenv()

BOT_TOKEN = settings.BOT_TOKEN
if not BOT_TOKEN:
    raise RuntimeError("Не найден BOT_TOKEN в .env")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(start_router)
dp.include_router(recording_router)
dp.include_router(menu_router)
dp.include_router(user_router)
# dp.include_router(diagnostic_router)


async def on_startup():
    await init_db()
    logging.info("Database initialized")


def main():
    asyncio.run(on_startup())
    dp.run_polling(bot)


if __name__ == "__main__":
    main()
