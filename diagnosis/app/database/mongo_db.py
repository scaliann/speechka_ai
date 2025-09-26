from dataclasses import dataclass

from motor import motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings


@dataclass
class _AppContext:
    """Application context."""

    mongo_client: AsyncIOMotorClient = None


ctx = _AppContext()


async def setup_mongodb() -> None:
    """
    Открыть соединение с MongoDB
    """
    if not settings.mongo_db:
        return
    ctx.mongo_client = motor_asyncio.AsyncIOMotorClient(settings.mongo_db)


async def close_mongodb() -> None:
    """
    Закрыть соединение с MongoDB
    """
    if ctx.mongo_client:
        ctx.mongo_client.close()
        ctx.mongo_client = None
