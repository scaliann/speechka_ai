from aiogram.fsm.state import State, StatesGroup


class TermsAgreement(StatesGroup):
    waiting_for_agreement = State()
