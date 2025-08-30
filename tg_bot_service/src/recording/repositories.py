import datetime as dt

from sqlalchemy import Result, func, select, result_tuple
from .models import Recording, RecordingSession, SessionStatus
from src.repositories import BaseRepo


class RecordingRepository(BaseRepo):

    async def next_number_for_user(self, user_id: int) -> int:
        """Возвращает n+1, где n — текущее число записей пользователя."""
        cnt = await self.session.scalar(
            select(func.count())
            .select_from(Recording)
            .where(Recording.user_id == user_id)
        )
        return (cnt or 0) + 1

    async def create(
        self,
        session_id: int,
        user_id: int,
        word_id: int,
        file_path: str = "",
    ) -> Recording:
        rec = Recording(
            session_id=session_id,
            user_id=user_id,
            word_id=word_id,
            file_path=str(file_path),
        )
        self.session.add(rec)
        await self.session.commit()
        await self.session.refresh(rec)
        return rec

    async def count_in_session(
        self,
        session_id: int,
    ) -> int:
        query = (
            select(func.count())
            .select_from(Recording)
            .where(Recording.session_id == session_id)
        )
        return await self.session.scalar(query)

    async def get_all_user_session(self, user_id: int):
        query = (
            select(
                RecordingSession,
            )
            .where(
                RecordingSession.user_id == user_id,
            )
            .order_by(
                RecordingSession.session_number,
            )
        )
        result: Result = await self.session.execute(query)
        sessions: RecordingSession = result.scalars()
        return list(sessions)

    async def get_paths_by_session(self, session_id: int) -> list[str]:
        stmt = (
            select(Recording.file_path)
            .where(Recording.session_id == session_id)
            .order_by(Recording.word_id)
        )
        return list(await self.session.scalars(stmt))


class SessionRepository(BaseRepo):
    async def get_active(
        self,
        user_id: int,
    ) -> RecordingSession | None:
        query = select(RecordingSession).where(
            RecordingSession.user_id == user_id,
            RecordingSession.status == SessionStatus.active,
        )
        result: Result = await self.session.execute(query)
        active_session: RecordingSession = result.scalar()
        return active_session

    async def create(self, user_id: int) -> RecordingSession:
        """Создаёт новую сессию и присваивает порядковый номер."""
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

    async def complete(self, session: RecordingSession):
        session.status = SessionStatus.completed
        session.finished_at = func.now()
        await self.session.commit()

