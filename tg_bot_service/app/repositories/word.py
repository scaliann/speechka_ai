from sqlalchemy import select, Result

from app.repositories.base import BaseRepository
from app.models.words import Word


class WordRepository(BaseRepository):
    async def get_list_words(
        self,
    ) -> list[Word]:
        query = select(
            Word,
        ).order_by(
            Word.id,
        )

        result: Result = await self.session.execute(query)
        words = result.scalars()
        return list(words)
