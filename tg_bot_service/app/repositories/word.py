from sqlalchemy import select, Result

from app.base_repository import BaseRepository
from app.models.words import Word


class WordRepository(BaseRepository):
    async def list_words(
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
