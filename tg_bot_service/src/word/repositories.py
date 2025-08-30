from sqlalchemy import select
from .models import Word
from src.repositories import BaseRepo


class WordRepository(BaseRepo):
    async def list_words(self) -> list[Word]:
        result = await self.session.scalars(select(Word).order_by(Word.id))
        return list(result)
