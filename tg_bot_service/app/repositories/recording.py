import datetime as dt

from sqlalchemy import Result, func, select, result_tuple
from app.base_repository import BaseRepository
from app.common.enums import SessionStatus
from app.models.recording import Recording
from app.models.recording_session import RecordingSession


class RecordingRepository(BaseRepository):

    async def next_number_for_user(
        self,
        user_id: int,
    ) -> int:
        """Возвращает n+1, где n — текущее число записей пользователя."""
        query = (
            select(
                func.count(),
            )
            .select_from(
                Recording,
            )
            .where(
                Recording.user_id == user_id,
            )
        )
        result = await self.session.execute(query)
        count = result.scalar()
        return (count or 0) + 1

    async def create(
        self,
        session_id: int,
        user_id: int,
        word_id: int,
        file_path: str = "",
    ) -> Recording:
        """Создать объект Recording"""
        recording = Recording(
            session_id=session_id,
            user_id=user_id,
            word_id=word_id,
            file_path=str(file_path),
        )
        self.session.add(recording)
        await self.session.commit()
        await self.session.refresh(recording)
        return recording

    async def count_in_session(
        self,
        session_id: int,
    ) -> int:
        """Получить количество записей в сессии по session_id"""
        query = (
            select(
                func.count(),
            )
            .select_from(
                Recording,
            )
            .where(
                Recording.session_id == session_id,
            )
        )
        return await self.session.scalar(query)

    async def get_all_user_session(
        self,
        user_id: int,
    ) -> list[Recording]:
        """Получить все сессии пользователя по user_id"""
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
        sessions = result.scalars()
        return list(sessions)

    async def get_paths_by_session(
        self,
        session_id: int,
    ) -> list[str]:
        """Получить список путей файлов записи по id сессии"""
        query = (
            select(
                Recording.file_path,
            )
            .where(
                Recording.session_id == session_id,
            )
            .order_by(
                Recording.word_id,
            )
        )
        result: Result = await self.session.execute(query)
        paths = result.scalars()
        return list(paths)
