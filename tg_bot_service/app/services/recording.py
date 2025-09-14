from pathlib import Path
from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

from aiogram.types import Voice

from app.common.enums import SessionStatus
from app.common.utils import save_voice_to_mongo
from app.fms.recording_state import Recording
from app.keyboards.menu import kb_menu
from app.models.recording_session import RecordingSession
from app.models.user import User
from app.models.words import Word
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.repositories.mongo import MongoRecordingsRepository
from app.repositories.recording import RecordingRepository
from app.repositories.recording_session import SessionRepository
from app.repositories.user import UserRepository
from app.repositories.word import WordRepository


class RecordingService:
    """Инкапсулирует бизнес‑логику записи и сохранения голосовых."""

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session
        self.user_repository = UserRepository(session)
        self.word_repository = WordRepository(session)
        self.recording_repository = RecordingRepository(session)
        self.recording_session_repository = SessionRepository(session)

    async def start_recording(
        self,
        msg: Message,
        state: FSMContext,
    ) -> None:
        """Начало записи. Обновляем stage"""

        user, recording_session, words = await self.start_session(msg.from_user.id)
        await state.update_data(
            session_id=recording_session.id,
            word_ids=[w.id for w in words],
            words=[w.text for w in words],
            idx=0,
            user_id=user.id,
        )

        await msg.answer(
            f"🗝️ Сессия №{recording_session.session_number} открыта!\n\n🎯 Квест-предложение 1 из {len(words)}: <b>«{words[0].text}»</b>.\nНажми запись и произнеси его громко-смело, чтобы зарядить свой магический кристалл голоса! 🎙️",
            reply_markup=kb_menu,
            parse_mode="HTML",
        )
        await state.set_state(Recording.waiting_voice)

    async def start_session(
        self,
        tg_id: int,
    ) -> tuple[User, RecordingSession, list[Word]]:
        """
        Ищем текущую сессию пользователя
        и возвращаем пользователя, его текущую сессию и все слова
        """
        user = await self.user_repository.get_user(tg_id)
        if not user:
            user = await self.user_repository.create_user(tg_id)

        recording_session = await self.recording_session_repository.get_active(user.id)
        if recording_session is None:
            recording_session = await self.recording_session_repository.create(user.id)

        words = await self.word_repository.get_list_words()
        return user, recording_session, words

    async def save_recording(
        self,
        bot: Bot,
        voice: Voice,
        recording_session_id: int,
        user_id: int,
        tg_id: int,
        word_id: int,
        total_words: int,
    ) -> bool:
        """Функция отвечает за сохранение голосового"""
        file_path = await save_voice_to_mongo(
            bot=bot,
            voice=voice,
            tg_id=tg_id,
            recording_session_id=recording_session_id,
            word_id=word_id,
        )

        await self.recording_repository.create(
            recording_session_id=recording_session_id,
            user_id=user_id,
            word_id=word_id,
            file_path=file_path,
        )

        word_count = await self.recording_repository.count_in_session(
            recording_session_id
        )
        if word_count >= total_words:
            recording_session = await self.recording_session_repository.get_active(
                user_id
            )
            if recording_session and recording_session.id == recording_session_id:
                await self.recording_session_repository.update_status(
                    status=SessionStatus.completed,
                    recording_session_id=recording_session.id,
                )
                return True
        return False

    async def update_status(
        self,
        recording_session_id: int,
        status: SessionStatus,
    ) -> None:
        await self.recording_session_repository.update_status(
            recording_session_id=recording_session_id,
            status=status,
        )
