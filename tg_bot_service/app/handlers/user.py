from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text == "Профиль")
async def show_main_menu(message: Message):
    await message.answer("Ваш профиль: ")
