from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_training import UserTraining
from app.repositories.user_tongue_twister import UserTongueTwisterRepository
from app.repositories.user_training import UserTrainingRepository


class UserTrainingService:
    """Инкапсулирует бизнес‑логику пар пользователь - скороговорка."""

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session
        self.user_training_repository: UserTrainingRepository = UserTrainingRepository(
            session,
        )

    async def create(
        self,
        user_id: int,
        training_id: int,
    ) -> int:
        return await self.user_training_repository.create(
            user_id=user_id,
            training_id=training_id,
        )

    async def set_done(
        self,
        done_user_training_id: int,
    ):
        return await self.user_training_repository.set_done(
            done_user_training_id=done_user_training_id,
        )
