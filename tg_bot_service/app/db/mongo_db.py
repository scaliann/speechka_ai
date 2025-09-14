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
    """Инициализация Mongo как у вас: ctx + settings."""
    if not settings.MONGO_URI:
        return
    ctx.mongo_client = motor_asyncio.AsyncIOMotorClient(settings.MONGO_URI)


async def close_mongodb() -> None:
    if ctx.mongo_client:
        ctx.mongo_client.close()
        ctx.mongo_client = None
