from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def build_ikb_access_user_agreement() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Принимаю", callback_data="agreement:access")
    return kb.as_markup()


def build_ikb_training_actions() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🎙 Начать запись", callback_data="rec:start")
    kb.button(text="🧪 Диагностика", callback_data="diag:show")
    kb.button(text="🎯 Тренировочные задания", callback_data="test:test")
    kb.button(text="🌀 Скороговорки", callback_data="test:test")
    kb.button(text="💰 Оплата", callback_data="diag:run")
    kb.button(text="📖 Подробнее", callback_data="details:open")
    kb.adjust(1)
    return kb.as_markup()


def build_ikb_open_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🧭 Меню", callback_data="menu:open")
    return kb.as_markup()


def build_ikb_abort_session() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="✋ Прервать сессию", callback_data="session:abort")
    return kb.as_markup()
