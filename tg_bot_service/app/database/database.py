from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config import settings
from typing import AsyncGenerator

from app.models.base import Base

from app.models.tongue_twister import TongueTwister

DATABASE_URL = settings.database_url

async_engine = create_async_engine(settings.database_url, echo=False)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Get session."""
    async with (
        async_engine.begin() as connection,
        async_session_maker(bind=connection) as session,
    ):
        yield session


async def init_db() -> None:
    async with async_engine.begin() as conn:
        # Create all tables in the database
        await conn.run_sync(Base.metadata.create_all)

    from app.database.seed_values.seed_words import seed_basic_words
    from app.database.seed_values.seed_tongue_twisters import seed_tongue_twisters

    await seed_basic_words()
    await seed_tongue_twisters()
