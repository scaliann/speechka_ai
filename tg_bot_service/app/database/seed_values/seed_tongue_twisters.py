from sqlalchemy import select

from app.database.database import get_async_session
from app.models.tongue_twister import TongueTwister
from app.content.tongue_twisters import tongue_twisters


async def seed_tongue_twisters() -> None:
    """Гарантирует наличие базового списка слов."""
    async with get_async_session() as session:
        existing = set(await session.scalars(select(TongueTwister.text)))
        for w in tongue_twisters:
            if w not in existing:
                session.add(TongueTwister(text=w))
        await session.commit()
