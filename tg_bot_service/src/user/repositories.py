from sqlalchemy import Result, select
from .models import User
from src.repositories import BaseRepo


class UserRepository(BaseRepo):
    async def get_or_create(
        self,
        tg_id: int,
    ) -> User:
        query = select(User).where(User.tg_id == tg_id)
        result: Result = await self.session.execute(query)
        user = result.scalar()
        if user is None:
            user = User(tg_id=tg_id)
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
        return user
