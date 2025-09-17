from aiogram import Router, F, types
from app.content.menu_command_text import menu_command_text
from app.keyboards.menu import build_ikb_training_actions

router = Router()


@router.callback_query(F.data == "menu:open")
async def show_main_menu(
    cq: types.CallbackQuery,
) -> None:
    await cq.message.answer(
        menu_command_text,
        reply_markup=build_ikb_training_actions(),
    )
