from aiogram.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.db.database import get_async_session

CB_MENU_OPEN = "menu:open"
CB_DIAG_SESSION_PREFIX = "diag:session:"


def build_ikb_user_sessions(sessions) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for s in sessions:
        kb.button(
            text=f"Сессия {s.session_number}",
            callback_data=f"{CB_DIAG_SESSION_PREFIX}{s.id}",
        )
    kb.adjust(2)  # по 2 в ряд (хочешь — поставь 1)
    kb.row(InlineKeyboardButton(text="⬅️ Меню", callback_data=CB_MENU_OPEN))
    return kb.as_markup()
