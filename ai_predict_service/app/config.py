import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path


load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")


class Settings(BaseSettings):
    MONGO_URI: str
    mongodb_recordings_db: str = "speechka"
    mongodb_recordings_bucket: str = "recordings"

    class Config:
        env_file = "../.env"


settings = Settings()
