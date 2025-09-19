from sqlalchemy.ext.asyncio import AsyncSession

from app.content.user_agreement_command_text import user_agreement_command_text
from app.fms.terms_agreement_state import UserAgreement
from app.keyboards.menu import build_ikb_access_user_agreement
from app.models.user import User
from app.repositories.user import UserRepository
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery


class UserService:
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session
        self.user_repository = UserRepository(session)

    async def check_user_agreement(
        self,
        tg_id: int,
    ) -> bool:
        """Проверяет, согласился ли пользователь с условиями"""
        user = await self.user_repository.get_or_create(tg_id)
        return user.agreed_to_terms

    async def show_user_agreement(
        self,
        cq: CallbackQuery,
        state: FSMContext,
    ) -> None:
        """Показывает пользовательское соглашение"""
        await cq.message.answer(
            user_agreement_command_text,
            reply_markup=build_ikb_access_user_agreement(),
            parse_mode="Markdown",
        )
        await state.set_state(UserAgreement.waiting_for_agreement)

    async def get_or_create(
        self,
        tg_id: int,
    ) -> User:
        return await self.user_repository.get_or_create(tg_id)

    async def set_agreed(
        self,
        tg_id: int,
    ) -> None:
        await self.user_repository.set_agreed(tg_id=tg_id)
