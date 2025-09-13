from sqlalchemy import Result, select

from app.repositories.base import BaseRepository
from app.models.recording_session import RecordingSession


class DiagnosisRepository(BaseRepository):

    async def get_last_five_users_sessions(
        self, user_id: int
    ) -> list[RecordingSession]:
        """
        Возвращает все сессии данного пользователя,
        упорядоченные по session_number.
        """
        query = (
            select(RecordingSession)
            .where(RecordingSession.user_id == user_id)
            .order_by(
                RecordingSession.session_number.desc(),
            )
            .limit(5)
        )
        result: Result = await self.session.execute(query)
        user_sessions: list[RecordingSession] = result.scalars().all()
        return user_sessions

    async def get_by_number(
        self, user_id: int, session_number: int
    ) -> RecordingSession | None:
        stmt = select(RecordingSession).where(
            RecordingSession.user_id == 1,
            RecordingSession.session_number == session_number,
        )
        return await self.session.scalar(stmt)
