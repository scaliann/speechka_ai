from datetime import datetime, timedelta, timezone
from io import BytesIO
from pathlib import Path
from aiogram import Bot
from aiogram.types import Voice
from pydub import AudioSegment

from app.repositories.mongo import MongoRecordingsRepository


def utc_plus_3() -> datetime:
    """Возвращает текущее время + 3 ч, привязанное к UTC+3."""
    return datetime.now(timezone.utc) + timedelta(hours=3)


RECORDS_DIR = Path(__file__).resolve().parent.parent.parent.parent / "records"

TARGET_SR = 44100


async def save_voice_to_mongo(
    bot: Bot,
    voice: Voice,
    tg_id: int,
    recording_session_id: int,
    word_id: int,
) -> str:
    ogg_buf = BytesIO()
    t_file = await bot.get_file(voice.file_id)
    await bot.download(file=t_file, destination=ogg_buf)
    ogg_buf.seek(0)

    audio = AudioSegment.from_file(ogg_buf, format="ogg")
    audio = audio.set_channels(1).set_frame_rate(TARGET_SR).set_sample_width(2)
    wav_buf = BytesIO()
    audio.export(
        wav_buf,
        format="wav",
        codec="pcm_s16le",
        parameters=["-ar", str(TARGET_SR), "-ac", "1"],
    )
    wav_buf.seek(0)
    wav_bytes = wav_buf.read()

    mongo_repository = MongoRecordingsRepository()
    file_id = await mongo_repository.save_wav(
        data=wav_bytes,
        tg_id=tg_id,
        session_id=recording_session_id,
        word_id=word_id,
    )
    return str(file_id)
