import asyncio
import logging


from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats, MenuButtonDefault
from dotenv import load_dotenv

from app.db.mongo_db import setup_mongodb
from config import settings
from db.database import init_db
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


async def setup_menu(bot: Bot):
    await bot.set_my_commands(
        commands=[
            BotCommand(command="start", description="🏠 Главное меню"),
            BotCommand(command="help", description="❓ Помощь 📖"),
            BotCommand(command="privacy", description="🏛️ Конфиденциальность"),
        ],
        scope=BotCommandScopeAllPrivateChats(),
    )
    await bot.set_chat_menu_button(menu_button=MenuButtonDefault())


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
