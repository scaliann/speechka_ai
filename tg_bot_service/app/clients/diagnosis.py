from app.clients.base import BaseClient
from app.clients.requests.diagnosis import DiagnosisRequest
from app.clients.responses.diagnosis import DiagnosisResponse
from app.config import settings


class DiagnosisClient(BaseClient):
    def __init__(self):
        super().__init__(settings.diagnosis_host)

    async def get_diagnosis(
        self,
        data: DiagnosisRequest,
    ) -> DiagnosisResponse:
        return await self.request(
            path=f"/diagnose",
            method="POST",
            json=data.model_dump(),
            response_model=DiagnosisResponse,
            raise_for_status=True,
        )
