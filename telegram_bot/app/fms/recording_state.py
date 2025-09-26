from aiogram.fsm.state import State, StatesGroup


class Recording(StatesGroup):
    waiting_voice = State()
