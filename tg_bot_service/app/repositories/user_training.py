from sqlalchemy import insert, update

from app.models.user_training import UserTraining
from app.repositories.base import BaseRepository


class UserTrainingRepository(
    BaseRepository,
):
    async def create(
        self,
        user_id: int,
        training_id: int,
    ) -> int:
        query = (
            insert(
                UserTraining,
            )
            .values(
                user_id=user_id,
                training_id=training_id,
            )
            .returning(
                UserTraining.id,
            )
        )

        result = await self.session.execute(query)
        return result.scalar_one()

    async def set_done(
        self,
        done_user_training_id: int,
    ):
        query = (
            update(
                UserTraining,
            )
            .values(
                is_done=True,
            )
            .where(
                UserTraining.id == done_user_training_id,
            )
        )
        await self.session.execute(query)
