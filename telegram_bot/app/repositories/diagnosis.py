from app.common.enums import DiagnosisResult
from app.common.utils import utc_plus_3
from app.models.diagnosis import Diagnosis
from app.repositories.base import BaseRepository
from sqlalchemy import insert


class DiagnosisRepository(BaseRepository):
    async def save_diagnosis(
        self,
        diagnosis: str,
        results: str,
        user_id: int,
        recording_session_id: int,
    ) -> int:
        """
        Создаёт запись в diagnosis и возвращает её id.
        """
        query = (
            insert(
                Diagnosis,
            )
            .values(
                user_id=user_id,
                recording_session_id=recording_session_id,
                diagnosis=diagnosis,
                results=results,
                finished_at=utc_plus_3(),
            )
            .returning(
                Diagnosis.id,
            )
        )

        result = await self.session.execute(query)
        return result.scalar_one()
