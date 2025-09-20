from aiogram import Router, F
from aiogram.types import CallbackQuery, BufferedInputFile, FSInputFile

from app.clients.diagnosis import DiagnosisClient
from app.clients.requests.diagnosis import DiagnosisRequest

from app.database.database import get_async_session
from app.keyboards.sessions import build_ikb_user_sessions
from pathlib import Path

from app.repositories.user import UserRepository
from app.services.recording import RecordingService
from app.services.recording_session import RecordingSessionService
import re

from app.services.user import UserService

router = Router()

BASE_DIR = Path(__file__).parent.parent
PDF_PATH = BASE_DIR / "templates/pdf.pdf"


@router.callback_query(F.data == "diag:show")
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


@router.callback_query(F.data.regexp(r"^diag:session:(\d+)$"))
async def handle_session_result_cq(cq: CallbackQuery):
    """Пользователь нажал кнопку «Сессия N»."""

    try:
        m = re.match(r"^diag:session:(\d+)$", cq.data or "")
        session_number = int(m.group(1))
    except ValueError:
        await cq.message.answer("Номер сессии не распознан.")
        return

    async with get_async_session() as session:
        recording_session_service = RecordingSessionService(session)
        recording_service = RecordingService(session)
        user_service = UserService(session)

        user = await user_service.get_or_create(cq.from_user.id)
        recording_session = await recording_session_service.get_by_number(
            user_id=user.id,
            session_number=session_number,
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
    results = await DiagnosisClient().get_diagnosis(data=data)

    doc = FSInputFile(
        PDF_PATH,
        filename="report.pdf",
    )

    await cq.message.answer_document(
        document=doc,
        caption=f"Ваш PDF 📄. Результат: {results}",
    )
