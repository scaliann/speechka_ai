import asyncio
from app.database.mongo_db import setup_mongodb
from app.repositories.mongo import MongoRepository
from app.services.diagnosis import DiagnosisService


async def main():
    await setup_mongodb()
    mongo_repository = MongoRepository()
    diagnnosis_service = DiagnosisService()
    list_ids = await mongo_repository.list_ids()
    print(list_ids)
    diagnosis = await diagnnosis_service.predict_all(list_ids)
    idx1 = len(diagnosis) - 1
    idx2 = len(diagnosis)
    print(diagnosis)
    return list_ids


if __name__ == "__main__":
    asyncio.run(main())
