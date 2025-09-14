from sqlalchemy.ext.asyncio import AsyncSession


from app.common.enums import SessionStatus
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
