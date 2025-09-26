from sqlalchemy import select, Result, insert

from app.models.user_tongue_twister import UserTongueTwister
from app.repositories.base import BaseRepository
from app.models.tongue_twister import TongueTwister


class UserTongueTwisterRepository(BaseRepository):
    async def create(
        self,
        user_id: int,
        tongue_twister_id: int,
    ) -> None:
        query = insert(
            UserTongueTwister,
        ).values(
            user_id=user_id,
            tongue_twister_id=tongue_twister_id,
        )

        await self.session.execute(query)

    async def get_done(
        self,
        user_id: int,
    ):
        query = select(
            UserTongueTwister,
        ).where(
            UserTongueTwister.user_id == user_id,
        )
        result = await self.session.execute(query)
        return result.scalars().all()
