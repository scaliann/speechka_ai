from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy import update
from app.config import settings
from typing import AsyncGenerator


from app.models import Base

from app.word import models
from app.recording import models
from app.user import models

DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(settings.DATABASE_URL, echo=False)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def update_existing_users():
    """Обновляет всех существующих пользователей, устанавливая agreed_to_terms = True"""
    async with get_async_session() as session:
        # Обновляем всех пользователей, у которых agreed_to_terms = False или NULL
        stmt = (
            update(models.User)
            .where(models.User.agreed_to_terms.is_(None) | (models.User.agreed_to_terms == False))
            .values(agreed_to_terms=True)
        )
        result = await session.execute(stmt)
        await session.commit()

        if result.rowcount > 0:
            print(f"Обновлено существующих пользователей: {result.rowcount}")


async def init_db() -> None:
    async with engine.begin() as conn:
        # Create all tables in the database
        await conn.run_sync(Base.metadata.create_all)

    # Обновляем существующих пользователей
    await update_existing_users()

    from app.db.seed_words import seed_basic_words

    await seed_basic_words()
