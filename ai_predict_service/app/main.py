from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.diagnosis import diagnosis_router
from app.database.mongo_db import setup_mongodb


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    await setup_mongodb()
    yield


app = FastAPI(
    title="AI Predict Service", description="Сервис для анализа речи", lifespan=lifespan
)

app.include_router(diagnosis_router)


@app.get("/status")
async def health_check():
    return {
        "status": "ok",
    }
