from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

from app.db.database import get_async_session
from app.diagnostic.services import DiagnosisService


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
        one_time_keyboard=True,
    )

    return kb
