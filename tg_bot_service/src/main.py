import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from config import settings
from db.db_helper import init_db
from recording.handlers import router as record_router
from menu.handlers import router as menu_router
from user.handlers import router as user_router, check_user_agreement, show_terms_agreement
from src.keyboards.menu import kbs_menu, kb_menu
from src.content.content import start_command_text
from src.diagnostic.handlers import router as diagnostic_router

load_dotenv()

BOT_TOKEN = settings.BOT_TOKEN
if not BOT_TOKEN:
    raise RuntimeError("Не найден BOT_TOKEN в .env")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(record_router)
dp.include_router(menu_router)
dp.include_router(user_router)
dp.include_router(diagnostic_router)


@dp.message(CommandStart())
async def cmd_start(message: Message):
    # Проверяем, согласился ли пользователь с условиями
    agreed = await check_user_agreement(message.from_user.id)

    if not agreed:
        # Если не согласился, показываем соглашение
        await show_terms_agreement(
            message,
            dp.fsm.get_context(
                bot=message.bot, user_id=message.from_user.id, chat_id=message.chat.id
            ),
        )
    else:
        # Если согласился, показываем главное меню
        await message.answer(
            start_command_text,
            reply_markup=kbs_menu,
        )


async def on_startup():
    await init_db()
    logging.info("Database initialized")


def main():
    asyncio.run(on_startup())
    dp.run_polling(bot)


if __name__ == "__main__":
    main()
