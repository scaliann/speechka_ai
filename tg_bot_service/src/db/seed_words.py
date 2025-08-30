from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.db.db_helper import get_async_session

from src.word.models import Word

WORDS = [
    "Рыжий рыцарь рубит рыбу",
    "Зоркий радар заметил ракету",
    "Карл крал кораллы у Клары",
    "Роза выросла на заре у ручья",
    "Зебра смело ступила за забор",
    "Быстрый барс проскочил через ограду",
    "Рыжий кот мурлычет на солнечной крыше",
    "Зоркая сова сторожит сказочный лес ночью",
    "Бодрый бобр строит плотину из ровных брёвен",
    "Смелый спасатель спас сверчка из лужи",
]


async def seed_basic_words() -> None:
    """Гарантирует наличие базового списка слов."""
    async with get_async_session() as session:
        existing = set(await session.scalars(select(Word.text)))
        for w in WORDS:
            if w not in existing:
                session.add(Word(text=w))
        await session.commit()
