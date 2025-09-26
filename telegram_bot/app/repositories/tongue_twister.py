from sqlalchemy import select
from app.repositories.base import BaseRepository
from app.models.tongue_twister import TongueTwister
from app.models.user_tongue_twister import UserTongueTwister


class TongueTwisterRepository(BaseRepository):
    async def get_free_tongue_twister(
        self,
        user_id: int,
    ):
        query = (
            select(
                TongueTwister,
            )
            .outerjoin(
                UserTongueTwister,
                (UserTongueTwister.tongue_twister_id == TongueTwister.id)
                & (UserTongueTwister.user_id == user_id),
            )
            .where(UserTongueTwister.id.is_(None))
            .order_by(
                TongueTwister.id,
            )
        )
        res = await self.session.execute(query)
        return res.scalars().all()
