from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.content.user_agreement_command_text import user_agreement_command_text
from app.database.database import get_async_session
from app.keyboards.menu import build_ikb_training_actions, build_ikb_open_menu
from app.services.user import UserService

router = Router()


@router.callback_query(F.data == "agreement:access")
async def agree_to_terms(
    cq: CallbackQuery,
    state: FSMContext,
) -> None:
    async with get_async_session() as session:
        user_service = UserService(session)
        user = await user_service.get_or_create(cq.from_user.id)
        await user_service.set_agreed(tg_id=user.tg_id)

    await state.clear()
    await cq.message.answer(
        "✅ Спасибо! Вы согласились с пользовательским соглашением.\n\n"
        "Теперь вы можете пользоваться всеми функциями бота!",
        reply_markup=build_ikb_training_actions(),
    )


@router.message(F.text == "/agreement")
async def show_agreement(
    message: Message,
) -> None:
    await message.answer(
        text=user_agreement_command_text,
        reply_markup=build_ikb_open_menu(),
    )
