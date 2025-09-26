from aiogram.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.database import get_async_session

CB_MENU_OPEN = "menu:open"
CB_DIAG_SESSION_PREFIX = "diagnosis:session:"


def build_ikb_user_sessions(
    sessions,
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for s in sessions:
        kb.button(
            text=f"Сессия {s.session_number}",
            callback_data=f"{CB_DIAG_SESSION_PREFIX}{s.id}",
        )
    kb.adjust(2)
    kb.row(InlineKeyboardButton(text="⬅️ Меню", callback_data=CB_MENU_OPEN))
    return kb.as_markup()
