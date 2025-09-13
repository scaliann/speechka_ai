from datetime import datetime, timedelta, timezone
from pathlib import Path
from aiogram import Bot
from aiogram.types import Voice
from pydub import AudioSegment


def utc_plus_3() -> datetime:
    """Возвращает текущее время + 3 ч, привязанное к UTC+3."""
    return datetime.now(timezone.utc) + timedelta(hours=3)


RECORDS_DIR = Path(__file__).resolve().parent.parent.parent.parent / "records"

TARGET_SR = 44100


async def save_voice(
    bot: Bot,
    voice: Voice,
    tg_id: int,
    recording_session_id: int,
    word_id: int,
) -> str:
    """Скачивает voice в .ogg, конвертирует в .wav (16 kHz/mono/PCM-16)
    и возвращает относительный путь records/{tg_id}/{session_id}/{word_id}.wav
    """

    user_dir = RECORDS_DIR / str(tg_id) / str(recording_session_id)
    user_dir.mkdir(parents=True, exist_ok=True)

    ogg_path = user_dir / f"{word_id}.ogg"
    wav_path = user_dir / f"{word_id}.wav"

    t_file = await bot.get_file(voice.file_id)
    await bot.download(file=t_file, destination=ogg_path)

    audio = AudioSegment.from_file(ogg_path, format="ogg")
    audio = audio.set_channels(1).set_frame_rate(TARGET_SR).set_sample_width(2)
    audio.export(
        wav_path,
        format="wav",
        codec="pcm_s16le",
        parameters=["-ar", str(TARGET_SR), "-ac", "1"],
    )

    ogg_path.unlink(missing_ok=True)

    relative_path = wav_path.relative_to(RECORDS_DIR.parent)
    return str(relative_path)
