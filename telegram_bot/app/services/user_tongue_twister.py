from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_tongue_twister import UserTongueTwisterRepository


class UserTongueTwisterService:
    """Инкапсулирует бизнес‑логику пар пользователь - скороговорка."""

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session
        self.user_tongue_twister_repository: UserTongueTwisterRepository = (
            UserTongueTwisterRepository(session)
        )

    async def create(
        self,
        user_id: int,
        tongue_twister_id: int,
    ) -> None:
        return await self.user_tongue_twister_repository.create(
            user_id=user_id,
            tongue_twister_id=tongue_twister_id,
        )

    async def get_done(
        self,
        user_id: int,
    ):
        return await self.user_tongue_twister_repository.get_done(
            user_id=user_id,
        )
