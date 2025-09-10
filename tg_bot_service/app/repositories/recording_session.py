from sqlalchemy import Result, func, select
from app.base_repository import BaseRepository
from app.common.enums import SessionStatus
from app.models.recording_session import RecordingSession


class SessionRepository(BaseRepository):
    async def get_active(
        self,
        user_id: int,
    ) -> RecordingSession | None:
        """Получить активную сессию по user_id"""
        query = select(
            RecordingSession,
        ).where(
            RecordingSession.user_id == user_id,
            RecordingSession.status == SessionStatus.active,
        )
        result: Result = await self.session.execute(query)
        active_session: RecordingSession = result.scalar()
        return active_session

    async def create(
        self,
        user_id: int,
    ) -> RecordingSession:
        """Создать новую сессию."""
        query = select(
            func.coalesce(func.max(RecordingSession.session_number), 0) + 1
        ).where(
            RecordingSession.user_id == user_id,
        )

        result: Result = await self.session.execute(query)
        next_num = result.scalar()
        session_obj = RecordingSession(user_id=user_id, session_number=next_num)
        self.session.add(session_obj)
        await self.session.commit()
        await self.session.refresh(session_obj)
        return session_obj

    async def complete(
        self,
        session: RecordingSession,
    ) -> None:
        """Поменять статус сессии на завершенный."""
        session.status = SessionStatus.completed
        session.finished_at = func.now()
        await self.session.commit()
