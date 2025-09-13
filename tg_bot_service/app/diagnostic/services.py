from sqlalchemy.ext.asyncio import AsyncSession

from app.diagnostic.repositories import DiagnosisRepository


class DiagnosisService:
    """Инкапсулирует бизнес‑логику диагностики."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.diagnosis_repo: DiagnosisRepository = DiagnosisRepository(session)

    async def get_last_five_users_sessions(self, user_id):
        return await self.diagnosis_repo.get_last_five_users_sessions(user_id)
