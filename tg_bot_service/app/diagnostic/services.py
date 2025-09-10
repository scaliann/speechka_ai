from pathlib import Path
from aiogram import Bot

from app.diagnostic.repositories import DiagnosisRepository
from app.user.repositories import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.word.repositories import WordRepository
from app.recording.repositories import RecordingRepository, SessionRepository
from aiogram.types import Voice
from app.recording.file_utils import save_voice


class DiagnosisService:
    """Инкапсулирует бизнес‑логику диагностики."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.diagnosis_repo: DiagnosisRepository = DiagnosisRepository(session)

    async def get_last_five_users_sessions(self, user_id):
        return await self.diagnosis_repo.get_last_five_users_sessions(user_id)
