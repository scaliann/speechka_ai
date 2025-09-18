from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.db.database import get_async_session
from app.keyboards.sessions import build_ikb_user_sessions
import httpx

from app.repositories.user import UserRepository
from app.services.recording_session import RecordingSessionService

router = Router()


async def send_for_diag(
    paths: list[str],
):
    # Transform relative paths to absolute paths for the AI services
    # The AI services expects paths relative to /app/records
    transformed_paths = []
    for path in paths:
        # Convert relative path like "records/693505334/2/1.wav" to "/app/records/693505334/2/1.wav"
        if path.startswith("records/"):
            # Remove "records/" prefix and add "/app/records/" prefix
            relative_path = path.replace("records/", "")
            transformed_path = f"/app/records/{relative_path}"
        else:
            transformed_path = path
        transformed_paths.append(transformed_path)

    async with httpx.AsyncClient(timeout=60) as c:
        resp = await c.post(
            "http://ai_predict_service:8000/diagnose", json=transformed_paths
        )
        resp.raise_for_status()
        return resp.json()


@router.callback_query(F.data == "diag:run")
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


# @router.message(F.text.regexp(r"^Сессия\s+\d+$"))
# async def handle_session_result(msg: Message):
#     """Пользователь нажал кнопку «Сессия N»."""
#
#     try:
#         session_number = int(msg.text.split()[-1])
#     except ValueError:
#         await msg.answer("Номер сессии не распознан.")
#         return
#
#     user_tg_id = msg.from_user.id
#
#     async with get_async_session() as db:
#         diag_repo = DiagnosisRepository(db)
#         rec_repo = RecordingRepository(db)
#
#         session_obj = await diag_repo.get_by_number(
#             user_id=user_tg_id,
#             session_number=session_number,
#         )
#         if not session_obj:
#             await msg.answer("Такой сессии не найдено.")
#             return
#
#         paths = await rec_repo.get_paths_by_session(session_obj.id)
#
#     if not paths:
#         await msg.answer("У этой сессии нет записей.")
#         return
#
#     result = await send_for_diag(paths)
#     diagnosis = result["diagnosis"]
#     recommendation = result["recommendation"]
#     logs = result["logs"]  # если хотите вывести/сохранить
#
#     # --- ответ пользователю ---
#     answer = f"Результат сессии {session_number}:\n\n{recommendation}"
#     await msg.answer(answer, disable_web_page_preview=True)
