from aiogram import Router, F
from aiogram.types import Message
from app.content.menu_command_text import menu_command_text
from app.keyboards.menu import kbs_menu

router = Router()


@router.message(F.text == "Меню")
async def show_main_menu(
    message: Message,
) -> None:
    await message.answer(
        menu_command_text,
        reply_markup=kbs_menu,
    )
