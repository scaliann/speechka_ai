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
        """Считать wav байты"""

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
    ) -> JSONResponse:
        """
        Найти один объекет по mongo_id.
        """

        oid = ObjectId(mongo_id)
        files = self.db[f"{settings.mongodb_recordings_bucket}.files"]
        doc = await files.find_one({"_id": oid})
        content = json.loads(json_util.dumps(doc))
        return JSONResponse(content=content)

    async def find_all(
        self,
    ) -> JSONResponse:
        """
        Получить все объекты записей в Mongo.
        """

        files = self.db[f"{settings.mongodb_recordings_bucket}.files"]
        cursor = files.find({}).sort([("_id", 1)])
        docs = [doc async for doc in cursor]
        content = json.loads(json_util.dumps(docs))
        return JSONResponse(content=content)

    async def list_ids(
        self,
    ) -> list[str]:
        """
        Получить список всех oid записей в Mongo.
        """

        files = self.db[f"{settings.mongodb_recordings_bucket}.files"]
        cur = files.find({}, {"_id": 1}).sort([("_id", 1)])
        return [str(doc["_id"]) async for doc in cur]
