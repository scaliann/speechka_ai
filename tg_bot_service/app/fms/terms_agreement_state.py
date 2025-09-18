from aiogram.fsm.state import State, StatesGroup


class UserAgreement(StatesGroup):
    waiting_for_agreement = State()
