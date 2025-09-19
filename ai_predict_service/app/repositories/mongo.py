import json

from bson import ObjectId, json_util
import io

from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from starlette.responses import JSONResponse

from app.config import settings
from app.database.mongo_db import ctx


class MongoRepository:
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
            self.db,
            bucket_name=settings.mongodb_recordings_bucket,
        )

    async def read_wav_bytes(
        self,
        mongo_id: str,
    ) -> bytes:
        oid = ObjectId(mongo_id)
        buf = io.BytesIO()
        await self.bucket.download_to_stream(oid, buf)
        await self.bucket.download_to_stream(
            oid,
            buf,
        )
        return buf.getvalue()

    async def find_one(
        self,
        mongo_id: str,
    ):
        oid = ObjectId(mongo_id)
        files = self.db[f"{settings.mongodb_recordings_bucket}.files"]
        doc = await files.find_one({"_id": oid})
        content = json.loads(json_util.dumps(doc))
        return JSONResponse(content=content)
