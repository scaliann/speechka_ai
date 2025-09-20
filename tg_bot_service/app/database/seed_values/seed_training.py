from sqlalchemy import select

from app.database.database import get_async_session
from app.content.training import training
from app.models.training import Training


async def seed_training() -> None:
    """Гарантирует наличие базового списка слов."""
    async with get_async_session() as session:
        existing = set(await session.scalars(select(Training.text)))
        for w in training:
            if w not in existing:
                session.add(Training(text=w))
        await session.commit()
