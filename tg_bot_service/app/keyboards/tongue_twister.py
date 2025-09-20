from aiogram.types import (
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


def build_ikb_tongue_twister_next() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="⏩ Следующая скороговорка", callback_data="tongue_twisters:show")
    kb.button(text="🧭 Меню", callback_data="menu:open")
    kb.adjust(1)
    return kb.as_markup()
