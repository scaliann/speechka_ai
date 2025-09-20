from aiogram import Router, F
from aiogram.types import CallbackQuery, BufferedInputFile, FSInputFile

from app.clients.diagnosis import DiagnosisClient
from app.clients.requests.diagnosis import DiagnosisRequest
from app.common.enums import DiagnosisResult

from app.database.database import get_async_session
from app.keyboards.sessions import build_ikb_user_sessions
from pathlib import Path

from app.repositories.user import UserRepository
from app.services.diagnosis import DiagnosisService
from app.services.recording import RecordingService
from app.services.recording_session import RecordingSessionService
import re

from app.services.user import UserService

router = Router()

BASE_DIR = Path(__file__).parent.parent
PDF_PATH = BASE_DIR / "templates/burr_recommendation.pdf"


@router.callback_query(F.data == "diagnosis:show")
async def show_diagnosis(
    cq: CallbackQuery,
):
    # ВСЁ, что трогает БД — внутри контекста
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
    """Пользователь нажал кнопку «Сессия N»."""

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
    data = DiagnosisRequest(mongo_ids=mongo_object_ids)
    diagnosis_response = await DiagnosisClient().get_diagnosis(data=data)

    async with get_async_session() as session:
        diagnosis_service = DiagnosisService(session)

        await diagnosis_service.save_diagnosis(
            diagnosis=diagnosis_response.diagnosis,
            results=str(diagnosis_response.results),
            user_id=user.id,
            recording_session_id=recording_session.id,
        )

    doc = FSInputFile(
        PDF_PATH,
        filename="report.pdf",
    )
    await cq.message.answer_document(
        document=doc,
        caption=f"Ваш PDF 📄. Результат: {diagnosis_response}",
    )
