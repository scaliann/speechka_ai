from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from app.content.menu_command_text import menu_command_text
from app.content.start_command_text import start_command_text
from app.keyboards.menu import kbs_menu

router = Router()


@router.message(CommandStart())
async def command_start(message: Message):
    await message.answer(
        start_command_text,
        reply_markup=kbs_menu,
    )
