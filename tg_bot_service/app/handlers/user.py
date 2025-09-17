from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.db.database import get_async_session
from app.repositories.user import UserRepository

router = Router()


@router.message(F.text == "Профиль")
async def show_main_menu(message: Message):
    await message.answer("Ваш профиль: ")


@router.message(F.text == "Согласен с пользовательским соглашением")
async def agree_to_terms(
    message: Message,
    state: FSMContext,
) -> None:
    async with get_async_session() as session:
        user_repository = UserRepository(session)
    user = await user_repository.get_or_create(message.from_user.id)
    user.agreed_to_terms = True
    await session.commit()

    await state.clear()
    await message.answer(
        "✅ Спасибо! Вы согласились с пользовательским соглашением.\n\n"
        "Теперь вы можете пользоваться всеми функциями бота!",
        reply_markup=kbs_menu,
    )
