from sqlalchemy import select

from app.db.db_helper import get_async_session
from app.models.words import Word
from app.content.words import WORDS


async def seed_basic_words() -> None:
    """Гарантирует наличие базового списка слов."""
    async with get_async_session() as session:
        existing = set(await session.scalars(select(Word.text)))
        for w in WORDS:
            if w not in existing:
                session.add(Word(text=w))
        await session.commit()
