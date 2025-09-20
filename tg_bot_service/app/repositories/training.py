from sqlalchemy import select

from app.models.training import Training
from app.models.user_training import UserTraining
from app.repositories.base import BaseRepository


class TrainingRepository(BaseRepository):
    async def get_free_trainings(
        self,
        user_id: int,
    ):
        query = (
            select(
                Training,
            )
            .outerjoin(
                UserTraining,
                (UserTraining.training_id == Training.id)
                & (UserTraining.user_id == user_id),
            )
            .where(UserTraining.id.is_(None))
            .order_by(
                UserTraining.id,
            )
        )
        res = await self.session.execute(query)
        return res.scalars().all()
