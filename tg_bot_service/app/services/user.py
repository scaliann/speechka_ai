from app.content.terms_command_text import terms_command_text
from app.db.db_helper import get_async_session
from app.fms.terms_agreement_state import TermsAgreement
from app.keyboards.menu import kb_terms
from app.repositories.user import UserRepository
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


class UserService:

    async def check_user_agreement(
        self,
        tg_id: int,
    ) -> bool:
        """Проверяет, согласился ли пользователь с условиями"""
        async with get_async_session() as session:
            repository = UserRepository(session)
            user = await repository.get_or_create(tg_id)
            return user.agreed_to_terms

    async def show_terms_agreement(
        self,
        message: Message,
        state: FSMContext,
    ) -> None:
        """Показывает пользовательское соглашение"""
        await message.answer(
            terms_command_text, reply_markup=kb_terms, parse_mode="Markdown"
        )
        await state.set_state(TermsAgreement.waiting_for_agreement)
