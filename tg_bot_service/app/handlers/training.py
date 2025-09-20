import random

from aiogram import Router, F, types
import re
from app.database.database import get_async_session
from app.keyboards.menu import build_ikb_open_menu
from app.keyboards.tongue_twister import build_ikb_tongue_twister_next
from app.keyboards.training import build_ikb_training_next
from app.repositories.user_training import UserTrainingRepository
from app.services.toungue_twister import TongueTwisterService
from app.services.training import TrainingService
from app.services.user import UserService
from app.services.user_tongue_twister import UserTongueTwisterService
from app.services.user_training import UserTrainingService

router = Router()


@router.callback_query(F.data == "training:show")
async def show_training(
    cq: types.CallbackQuery,
) -> None:
    async with get_async_session() as session:
        training_service = TrainingService(session)
        user_training_service = UserTrainingService(session)
        user_service = UserService(session)

        user = await user_service.get_or_create(tg_id=cq.from_user.id)
        trainings = await training_service.get_free_trainings(user.id)

        if not trainings:
            await cq.message.answer(
                "🎉 Поздравляем! Ты Выполнил все задания!",
                reply_markup=build_ikb_open_menu(),
            )
            return

        training = random.choice(trainings)
        user_training_id = await user_training_service.create(
            user_id=user.id,
            training_id=training.id,
        )

    await cq.message.answer(
        training.text,
        reply_markup=build_ikb_training_next(user_training_id=user_training_id),
    )


@router.callback_query(F.data.regexp(r"^training:done:(\d+)$"))
async def training_done(
    cq: types.CallbackQuery,
) -> None:
    m = re.match(r"^training:done:(\d+)$", cq.data or "")
    done_user_training_id = int(m.group(1))

    async with get_async_session() as session:
        training_service = TrainingService(session)
        user_training_service = UserTrainingService(session)
        user_service = UserService(session)

        await user_training_service.set_done(done_user_training_id)

        user = await user_service.get_or_create(tg_id=cq.from_user.id)
        trainings = await training_service.get_free_trainings(user.id)

        if not trainings:
            await cq.message.answer(
                "🎉 Поздравляем! Ты Выполнил все задания!",
                reply_markup=build_ikb_open_menu(),
            )
            return

        training = random.choice(trainings)
        user_training_id = await user_training_service.create(
            user_id=user.id,
            training_id=training.id,
        )

    await cq.message.answer(
        training.text,
        reply_markup=build_ikb_training_next(user_training_id=user_training_id),
    )
