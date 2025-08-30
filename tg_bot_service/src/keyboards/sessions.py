from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

from src.db.db_helper import get_async_session
from src.diagnostic.services import DiagnosisService


async def get_session_kbs(user_id):
    async with get_async_session() as session:
        service = DiagnosisService(session)

    user_sessions = await service.get_last_five_users_sessions(user_id)

    rows = [[KeyboardButton(text="Меню")]] + [
        [KeyboardButton(text=f"Сессия {s.session_number}")] for s in user_sessions
    ]

    kb = ReplyKeyboardMarkup(
        keyboard=rows,
        resize_keyboard=True,
        one_time_keyboard=True,  # кнопки уберутся после нажатия
    )

    return kb
