from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


kb_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Меню")]],
    resize_keyboard=True,
)

kbs_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Начать запись")],
        [KeyboardButton(text="Диагностика")],
    ],
    resize_keyboard=True,
)

kb_terms = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Согласен с пользовательским соглашением")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)
