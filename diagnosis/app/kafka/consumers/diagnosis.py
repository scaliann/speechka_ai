from app.kafka.schemas.diagnosis import DiagnosisSchema
from app.services.diagnosis import DiagnosisService


async def send_diagnosis_report(
    data: DiagnosisSchema,
) -> None:
    await DiagnosisService().get_and_send_diagnosis(data=data)
