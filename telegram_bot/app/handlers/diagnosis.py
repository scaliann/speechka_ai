from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile

from app.clients.diagnosis import DiagnosisClient
from app.clients.requests.diagnosis import DiagnosisRequest
from app.common.utils import get_report_path

from app.database.database import get_async_session
from app.kafka.producer import get_producer
from app.keyboards.sessions import build_ikb_user_sessions


from app.repositories.user import UserRepository
from app.services.diagnosis import DiagnosisService
from app.services.recording import RecordingService
from app.services.recording_session import RecordingSessionService
import re

import json
from app.services.user import UserService

router = Router()


@router.callback_query(F.data == "diagnosis:show")
async def show_diagnosis(
    cq: CallbackQuery,
) -> None:
    """
    Показывает пользователю 5 последних сессий в разделе "Диагностика."
    """
    async with get_async_session() as session:
        user = await UserRepository(session).get_or_create(cq.from_user.id)
        sessions = await RecordingSessionService(session).get_last_five_user_sessions(
            user.id
        )

    if not sessions:
        await cq.message.answer(
            "Пока нет записей для диагностики.\nСначала сделай короткую запись 🎙",
        )
        await cq.answer()
        return

    await cq.message.answer(
        "📜 Архив сессий — выбери любую, чтобы увидеть результат:",
        reply_markup=build_ikb_user_sessions(sessions),
    )
    await cq.answer()


@router.callback_query(F.data.regexp(r"^diagnosis:session:(\d+)$"))
async def handle_session_result_cq(cq: CallbackQuery):
    """
    Обработка сценария нажатия кнопки «Сессия N».
    Достаем по id сессии все нужные mongo_oid, tg_user_id
    и асинхронно отправляем их в diagnosis сервис через kafka.
    """

    try:
        m = re.match(r"^diagnosis:session:(\d+)$", cq.data or "")
        recording_session_id = int(m.group(1))
    except ValueError:
        await cq.message.answer("Номер сессии не распознан.")
        return

    async with get_async_session() as session:
        recording_session_service = RecordingSessionService(session)
        recording_service = RecordingService(session)
        user_service = UserService(session)

        user = await user_service.get_or_create(cq.from_user.id)
        recording_session = await recording_session_service.get_by_id(
            recording_session_id=recording_session_id,
        )
        if not recording_session:
            await cq.message.answer("Такой сессии не найдено.")
            return

        mongo_object_ids = await recording_service.get_mongo_objects_ids_by_session(
            recording_session.id
        )

    if not mongo_object_ids:
        await cq.message.answer("У этой сессии нет записей.")
        return

    data = DiagnosisRequest(
        mongo_object_ids=mongo_object_ids, chat_id=cq.message.chat.id, user_id=user.id
    )

    producer = get_producer()

    await cq.message.answer(
        "Мы уже начали диагностику! Как только все будет готово, ты получишь свой отчет!"
    )
    await producer.send_and_wait(
        topic="diagnosis_topic",
        value=json.dumps(data.model_dump()).encode("utf-8"),
    )
