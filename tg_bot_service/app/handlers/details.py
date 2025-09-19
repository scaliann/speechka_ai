from aiogram import Router, F, types

from app.content.details_command_answer_text import details_command_text
from app.keyboards.menu import build_ikb_training_actions

router = Router()


@router.callback_query(F.data == "details:open")
async def show_details(
    cq: types.CallbackQuery,
) -> None:
    await cq.message.answer(
        details_command_text,
        reply_markup=build_ikb_training_actions(),
    )
