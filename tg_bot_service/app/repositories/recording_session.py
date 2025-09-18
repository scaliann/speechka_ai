from sqlalchemy import Result, func, select, update
from app.repositories.base import BaseRepository
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
        active_recording_session: RecordingSession = result.scalar()
        return active_recording_session

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

    async def update_status(
        self,
        recording_session_id: int,
        status: SessionStatus,
    ) -> None:
        """Обновить статус сессии."""
        query = (
            update(
                RecordingSession,
            )
            .values(
                status=status,
            )
            .where(
                RecordingSession.id == recording_session_id,
            )
        )

        if status == SessionStatus.completed:
            query = (
                update(RecordingSession)
                .values(
                    finished_at=func.now(),
                    status=status,
                )
                .where(
                    RecordingSession.id == recording_session_id,
                )
            )
        await self.session.execute(query)

    async def get_last_five_user_sessions(
        self,
        user_id: int,
    ) -> list[RecordingSession]:
        """
        Возвращает все сессии данного пользователя,
        упорядоченные по session_number.
        """
        query = (
            select(
                RecordingSession,
            )
            .where(
                RecordingSession.user_id == user_id,
                RecordingSession.status == SessionStatus.completed,
            )
            .order_by(
                RecordingSession.session_number.desc(),
            )
            .limit(5)
        )
        result: Result = await self.session.execute(query)
        user_sessions: list[RecordingSession] = result.scalars().all()
        return user_sessions

    async def get_by_number(
        self,
        user_id: int,
        session_number: int,
    ) -> RecordingSession | None:
        stmt = select(
            RecordingSession,
        ).where(
            RecordingSession.user_id == user_id,
            RecordingSession.session_number == session_number,
        )
        return await self.session.scalar(stmt)
