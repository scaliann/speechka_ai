from aiogram.types import (
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


def build_ikb_training_next(
    user_training_id: int,
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="✔ Выполнено", callback_data=f"training:done:{user_training_id}")
    kb.button(text="🧭 Меню", callback_data="menu:open")
    kb.adjust(1)
    return kb.as_markup()
