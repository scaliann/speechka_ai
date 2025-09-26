from datetime import datetime
from io import BytesIO
from typing import Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from app.database.mongo_db import ctx, settings


class MongoRecordingsRepository:
    @property
    def db(
        self,
    ):
        return ctx.mongo_client[settings.mongodb_recordings_db]

    @property
    def bucket(
        self,
    ) -> AsyncIOMotorGridFSBucket:
        return AsyncIOMotorGridFSBucket(
            self.db, bucket_name=settings.mongodb_recordings_bucket
        )

    async def save_wav(
        self,
        data: bytes,
        tg_id: int,
        session_id: int,
        word_id: int,
    ) -> ObjectId:
        filename = f"{tg_id}/{session_id}/{word_id}.wav"
        metadata = {
            "tg_id": tg_id,
            "session_id": session_id,
            "word_id": word_id,
            "mime": "audio/wav",
            "sr": 48000,
            "channels": 1,
            "created_at": datetime.utcnow(),
        }
        file_id = await self.bucket.upload_from_stream(
            filename=filename,
            source=BytesIO(data),
            metadata=metadata,
        )
        return file_id

    async def read_wav(self, file_id: str | ObjectId) -> bytes:
        if isinstance(file_id, str):
            file_id = ObjectId(file_id)
        stream = await self.bucket.open_download_stream(file_id)
        try:
            return await stream.read()
        finally:
            await stream.close()
