from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.training import TrainingRepository


class TrainingService:
    """Инкапсулирует бизнес‑логику скороговорок."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.training_repository: TrainingRepository = TrainingRepository(session)

    async def get_free_trainings(
        self,
        user_id: int,
    ):
        return await self.training_repository.get_free_trainings(
            user_id=user_id,
        )

    async def get_all(
        self,
    ):
        return await self.training_repository.get_all()
