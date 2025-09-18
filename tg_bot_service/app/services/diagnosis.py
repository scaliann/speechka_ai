from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.diagnosis import DiagnosisRepository


class DiagnosisService:
    """Инкапсулирует бизнес‑логику диагностики."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.diagnosis_repository: DiagnosisRepository = DiagnosisRepository(session)
