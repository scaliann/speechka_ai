from sqlalchemy.ext.asyncio import AsyncSession

from app.common.enums import DiagnosisResult
from app.repositories.diagnosis import DiagnosisRepository


class DiagnosisService:
    """Инкапсулирует бизнес‑логику диагностики."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.diagnosis_repository: DiagnosisRepository = DiagnosisRepository(session)

    async def save_diagnosis(
        self,
        diagnosis: str,
        results: str,
        user_id: int,
        recording_session_id: int,
    ) -> int:
        return await self.diagnosis_repository.save_diagnosis(
            diagnosis=diagnosis,
            results=results,
            user_id=user_id,
            recording_session_id=recording_session_id,
        )
