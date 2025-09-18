from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from app.content.start_command_text import start_command_text
from app.keyboards.menu import build_ikb_open_menu

router = Router()


@router.message(CommandStart())
async def command_start(message: Message):
    await message.answer(
        start_command_text,
        reply_markup=build_ikb_open_menu(),
    )
