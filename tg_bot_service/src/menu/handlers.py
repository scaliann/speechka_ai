from aiogram import Router, F
from aiogram.types import Message
from aiohttp import request

from src.content.content import menu_command_text
from src.keyboards.menu import kbs_menu, kb_terms
from src.user.handlers import check_user_agreement, show_terms_agreement

router = Router()


@router.message(F.text == "Меню")
async def show_main_menu(message: Message):
    # Проверяем согласие пользователя
    agreed = await check_user_agreement(message.from_user.id)

    if not agreed:
        await show_terms_agreement(
            message,
            message.bot.fsm.get_context(
                bot=message.bot, user_id=message.from_user.id, chat_id=message.chat.id
            ),
        )
        return

    await message.answer(menu_command_text, reply_markup=kbs_menu)
