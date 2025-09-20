from sqlalchemy.ext.asyncio import AsyncSession


from app.common.enums import SessionStatus
from app.models.recording_session import RecordingSession
from app.repositories.recording_session import SessionRepository


class RecordingSessionService:
    """Инкапсулирует бизнес‑логику управления сессиями записей."""

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session
        self.recording_session_repository = SessionRepository(session)

    async def update_status(
        self,
        recording_session_id: int,
        status: SessionStatus,
    ) -> None:
        await self.recording_session_repository.update_status(
            recording_session_id=recording_session_id,
            status=status,
        )

    async def get_last_five_user_sessions(
        self,
        user_id: int,
    ) -> list[RecordingSession]:
        return await self.recording_session_repository.get_last_five_user_sessions(
            user_id=user_id
        )

    async def get_by_number(
        self,
        user_id: int,
        session_number: int,
    ) -> RecordingSession:
        return await self.recording_session_repository.get_by_number(
            user_id=user_id,
            session_number=session_number,
        )

    async def get_by_id(
        self,
        recording_session_id: int,
    ) -> RecordingSession:
        return await self.recording_session_repository.get_by_id(
            recording_session_id=recording_session_id,
        )
