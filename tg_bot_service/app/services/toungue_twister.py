from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.tongue_twister import TongueTwister
from app.repositories.tongue_twister import TongueTwisterRepository


class TongueTwisterService:
    """Инкапсулирует бизнес‑логику скороговорок."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.tongue_twister_repository: TongueTwisterRepository = (
            TongueTwisterRepository(session)
        )

    async def get_free_tongue_twister(
        self,
        user_id: int,
    ):
        return await self.tongue_twister_repository.get_free_tongue_twister(
            user_id=user_id,
        )

    async def get_all(
        self,
    ):
        query = select(
            TongueTwister,
        )
        result = await self.session.execute(query)
        return result.scalars().all()
