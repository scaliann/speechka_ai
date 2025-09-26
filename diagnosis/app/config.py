from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path


load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")


class Settings(BaseSettings):
    mongo_db: str = ""
    mongodb_recordings_db: str = ""
    mongodb_recordings_bucket: str = ""
    telegram_bot_token: str = ""
    kafka_host: str = ""

    class Config:
        env_file = "../.env"


settings = Settings()
