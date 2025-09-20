import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from app.database.mongo_db import setup_mongodb
from app.keyboards.left_bar_menu import setup_menu
from config import settings
from database.database import init_db
from handlers import (
    start_router,
    recording_router,
    menu_router,
    user_router,
    details_router,
    user_agreement_router,
    diagnosis_router,
    tongue_twister_router,
    training_router,
)

load_dotenv()

BOT_TOKEN = settings.telegram_bot_token
if not BOT_TOKEN:
    raise RuntimeError("Не найден BOT_TOKEN в .env")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(start_router)
dp.include_router(recording_router)
dp.include_router(menu_router)
dp.include_router(user_router)
dp.include_router(details_router)
dp.include_router(user_agreement_router)
dp.include_router(diagnosis_router)
dp.include_router(tongue_twister_router)
dp.include_router(training_router)


async def on_startup():
    await init_db()
    logging.info("Database initialized")
    await setup_mongodb()
    logging.info("Mongo initialized")
    await setup_menu(bot)


async def main():
    await on_startup()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
