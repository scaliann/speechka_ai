from pathlib import Path
from aiogram import Bot
from src.user.repositories import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.word.repositories import WordRepository
from src.recording.repositories import RecordingRepository, SessionRepository
from aiogram.types import Voice
from src.recording.file_utils import save_voice


class RecordingService:
    """Инкапсулирует бизнес‑логику диагностики."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)
        self.word_repo = WordRepository(session)
        self.rec_repo = RecordingRepository(session)
        self.sess_repo = SessionRepository(session)

    async def start_session(
        self,
        tg_id: int,
    ):
        """
        Ищем текущую сессию пользователя
        и возвращаем пользователя, его текущую сессию и все слова
        """
        user = await self.user_repo.get_or_create(tg_id)

        sess = await self.sess_repo.get_active(user.id)
        if sess is None:
            sess = await self.sess_repo.create(user.id)
        words = await self.word_repo.list_words()
        return user, sess, words

    async def save_recording(
        self,
        bot: Bot,
        voice: Voice,
        sess_id: int,
        user_id: int,
        tg_id: int,
        word_id: int,
        total_words: int,
    ) -> bool:
        """Функция отвечает за сохранение голосового"""
        number = await self.rec_repo.next_number_for_user(user_id)
        file_path: Path = await save_voice(
            bot=bot,
            voice=voice,
            tg_id=tg_id,
            session_id=sess_id,
            word_id=word_id,
        )
        await self.rec_repo.create(sess_id, user_id, word_id, file_path)

        cnt = await self.rec_repo.count_in_session(sess_id)
        if cnt >= total_words:
            sess = await self.sess_repo.get_active(user_id)
            if sess and sess.id == sess_id:
                await self.sess_repo.complete(sess)
                return True
        return False
