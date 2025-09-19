from typing import List

from fastapi import APIRouter, Body, Depends, Query

from app.api.requests.diagnosis import DiagnosisRequest
from app.api.responses.diagnosis import DiagnosisResponse
from app.repositories.mongo import MongoRepository
from app.services.diagnosis import DiagnosisService

diagnosis_router = APIRouter(tags=["Diagnosis"])


@diagnosis_router.post(
    path="/diagnose",
    response_model=DiagnosisResponse,
)
async def diagnose(
    data: DiagnosisRequest,
    service: DiagnosisService = Depends(),
) -> DiagnosisResponse:
    return await service.get_diagnosis(data)


@diagnosis_router.get(
    path="/get_object",
)
async def get(
    mongo_id: str = Query(...),
):
    mongo_repository = MongoRepository()
    result = await mongo_repository.find_one(mongo_id)
    return result
