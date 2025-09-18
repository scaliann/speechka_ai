from sqlalchemy import Result, select, update
from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    async def get_or_create(  # ToDo Разделить функцию на две - get и create и вынести бизнес логику в слой сервисов
        self,
        tg_id: int,
    ) -> User:
        """Получить или создать пользователя"""
        query = select(
            User,
        ).where(
            User.tg_id == tg_id,
        )
        result: Result = await self.session.execute(query)
        user = result.scalar()
        if user is None:
            user = User(tg_id=tg_id)
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
        return user

    async def get_user(
        self,
        tg_id: int,
    ) -> User:
        """Получить или создать пользователя"""
        query = select(
            User,
        ).where(
            User.tg_id == tg_id,
        )
        result: Result = await self.session.execute(query)
        user = result.scalar()
        return user

    async def create_user(
        self,
        tg_id: int,
    ) -> User:
        user = User(tg_id=tg_id)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def set_agreed(
        self,
        tg_id: int,
    ) -> None:
        query = (
            update(User)
            .values(agreed_to_terms=True)
            .where(
                User.tg_id == tg_id,
            )
        )
        await self.session.execute(query)
