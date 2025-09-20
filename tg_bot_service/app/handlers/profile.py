from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.common.utils import progress_bar
from app.database.database import get_async_session
from app.keyboards.menu import build_ikb_open_menu
from app.services.toungue_twister import TongueTwisterService
from app.services.training import TrainingService
from app.services.user import UserService
from app.services.user_tongue_twister import UserTongueTwisterService
from app.services.user_training import UserTrainingService

router = Router()


@router.callback_query(F.data == "profile:show")
async def show_profile(cq: CallbackQuery):
    async with get_async_session() as session:
        user_training_service = UserTrainingService(session)
        training_service = TrainingService(session)
        user_tongue_twister_service = UserTongueTwisterService(session)
        tongue_twister_service = TongueTwisterService(session)
        user_service = UserService(session)

        user = await user_service.get_or_create(cq.from_user.id)

        done_trainings = await user_training_service.get_done(user_id=user.id)
        all_trainings = await training_service.get_all()

        done_tongue_twister = await user_tongue_twister_service.get_done(
            user_id=user.id
        )
        all_tongue_twister = await tongue_twister_service.get_all()

    parts = [
        "🏆 <b>Профиль</b>",
        "",
        "🧠 <b>Тренировки</b>",
        progress_bar(
            done=len(done_trainings),
            total=len(all_trainings),
        ),
        "",
        "🌀 <b>Скороговорки</b>",
        progress_bar(done=len(done_tongue_twister), total=len(all_tongue_twister)),
    ]

    text = "\n".join(parts)

    await cq.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=build_ikb_open_menu(),
    )
