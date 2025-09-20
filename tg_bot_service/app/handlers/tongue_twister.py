import random

from aiogram import Router, F, types

from app.database.database import get_async_session
from app.keyboards.menu import build_ikb_open_menu
from app.keyboards.tongue_twister import build_ikb_tongue_twister_next
from app.services.toungue_twister import TongueTwisterService
from app.services.user import UserService
from app.services.user_tongue_twister import UserTongueTwisterService

router = Router()


@router.callback_query(F.data == "tongue_twisters:show")
async def show_tongue_twisters(
    cq: types.CallbackQuery,
) -> None:
    random_number = random.randint(1, 5)
    async with get_async_session() as session:
        tongue_twister_service = TongueTwisterService(session)
        user_tongue_twister_service = UserTongueTwisterService(session)
        user_service = UserService(session)

        user = await user_service.get_or_create(tg_id=cq.from_user.id)
        tongue_twisters = await tongue_twister_service.get_free_tongue_twister(user.id)
        if not tongue_twisters:
            await cq.message.answer(
                "🎉 Поздравляем! Ты прошел все скороговорки!",
                reply_markup=build_ikb_open_menu(),
            )
            return

        tongue_twister = random.choice(tongue_twisters)
        await user_tongue_twister_service.create(
            user_id=user.id,
            tongue_twister_id=tongue_twister.id,
        )

    await cq.message.answer(
        tongue_twister.text,
        reply_markup=build_ikb_tongue_twister_next(),
    )
