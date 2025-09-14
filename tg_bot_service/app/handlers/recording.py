from __future__ import annotations
import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.common.enums import SessionStatus
from app.content.finished_answer_text import finished_answer_text
from app.content.next_word_recording_answer_text import (
    get_next_word_recording_answer_text,
)
from app.content.recording_session_aborted_text import recording_session_aborted_text
from app.content.start_recording_answer_text import get_recording_answer_text
from app.db.database import get_async_session
from app.fms.recording_state import Recording
from app.keyboards.menu import kbs_menu, kb_menu
from app.services.recording import RecordingService
from app.services.recording_session import RecordingSessionService
from app.services.user import UserService

router = Router()
logger = logging.getLogger(__name__)


@router.message(F.text == "Начать запись")
async def start_recording(
    msg: Message,
    state: FSMContext,
) -> None:
    user_service = UserService()

    agreed = await user_service.check_user_agreement(tg_id=msg.from_user.id)
    if not agreed:
        await user_service.show_terms_agreement(msg, state)
        return

    async with get_async_session() as session:
        recording_service = RecordingService(session)
        user, recording_session, words = await recording_service.start_session(
            msg.from_user.id
        )

    await state.update_data(
        session_id=recording_session.id,
        word_ids=[w.id for w in words],
        words=[w.text for w in words],
        idx=0,
        user_id=user.id,
    )
    answer_text = get_recording_answer_text(
        recording_session_number=recording_session.session_number,
        words=words,
        word=words[0].text,
    )
    await msg.answer(
        text=answer_text,
        reply_markup=kb_menu,
        parse_mode="HTML",
    )
    await state.set_state(Recording.waiting_voice)


@router.message(Recording.waiting_voice, F.text == "Меню")
async def return_to_menu(
    msg: Message,
    state: FSMContext,
) -> None:
    data = await state.get_data()
    recording_session_id: int | None = data.get("session_id")

    async with get_async_session() as session:
        recording_session_service = RecordingSessionService(session)
        await recording_session_service.update_status(
            recording_session_id=recording_session_id,
            status=SessionStatus.aborted,
        )

    await state.clear()
    await msg.answer(
        text=recording_session_aborted_text,
        reply_markup=kbs_menu,
    )


@router.message(Recording.waiting_voice, F.voice)
async def handle_voice(msg: Message, state: FSMContext):
    data = await state.get_data()
    idx = data["idx"]
    word_ids = data["word_ids"]
    words_txt = data["words"]
    user_id = data["user_id"]
    recording_session_id = data["session_id"]

    async with get_async_session() as session:
        service = RecordingService(session)
        finished = await service.save_recording(
            bot=msg.bot,
            voice=msg.voice,
            recording_session_id=recording_session_id,
            user_id=user_id,
            word_id=word_ids[idx],
            tg_id=msg.from_user.id,
            total_words=len(word_ids),
        )

    logger.info("saved rec — session=%s word=%s", recording_session_id, word_ids[idx])

    if finished:
        await msg.answer(
            text=finished_answer_text,
            reply_markup=kbs_menu,
        )
        await state.clear()
        return

    idx += 1
    await state.update_data(idx=idx)

    answer_text = get_next_word_recording_answer_text(
        previous_word=words_txt[idx - 1],
        next_word=words_txt[idx],
        current_word_number=idx + 1,
        total_words_length=len(words_txt),
    )
    await msg.answer(
        text=answer_text,
        parse_mode="HTML",
        reply_markup=kb_menu,
    )


@router.message(Recording.waiting_voice)
async def handle_not_voice(msg: Message):
    await msg.answer(
        "Пожалуйста, пришли именно *голосовое сообщение*.", reply_markup=kb_menu
    )
