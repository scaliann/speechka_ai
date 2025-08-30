import asyncio, subprocess
from pathlib import Path
from aiogram import Bot
from aiogram.types import Voice
from pydub import AudioSegment

RECORDS_DIR = Path(__file__).resolve().parent.parent.parent.parent / "records"

TARGET_SR = 44100

# async def save_voice(bot: Bot, voice: Voice, tg_id: int, session_id, word_id: int) -> Path:
#     """Скачивает voice‑сообщение в records/{tg_id}/{session}/{word_id}.ogg и возвращает путь."""
#     user_dir = RECORDS_DIR / str(tg_id) / str(session_id)
#     user_dir.mkdir(parents=True, exist_ok=True)
#     file_path = user_dir / f"{word_id}.ogg"
#
#     file = await bot.get_file(voice.file_id)
#     await bot.download(file=file, destination=file_path)
#     return file_path


async def save_voice(
        bot: Bot,
        voice: Voice,
        tg_id: int,
        session_id: int,
        word_id: int
) -> str:
    """Скачивает voice в .ogg, конвертирует в .wav (16 kHz/mono/PCM-16)
    и возвращает относительный путь records/{tg_id}/{session_id}/{word_id}.wav
    """
    # ── директория ─────────────────────────────────────────────
    user_dir = RECORDS_DIR / str(tg_id) / str(session_id)
    user_dir.mkdir(parents=True, exist_ok=True)

    ogg_path = user_dir / f"{word_id}.ogg"
    wav_path = user_dir / f"{word_id}.wav"

    # ── 1. скачиваем .ogg из Telegram ─────────────────────────
    t_file = await bot.get_file(voice.file_id)
    await bot.download(file=t_file, destination=ogg_path)

    # ── 2. конвертируем с нужными параметрами ─────────────────
    audio = AudioSegment.from_file(ogg_path, format="ogg")
    audio = (
        audio
        .set_channels(1)               # mono
        .set_frame_rate(TARGET_SR)     # 16 kHz
        .set_sample_width(2)           # 16-bit PCM
    )
    audio.export(
        wav_path,
        format="wav",
        codec="pcm_s16le",             # гарантированно PCM-16-LE
        parameters=["-ar", str(TARGET_SR), "-ac", "1"]
    )

    # ── 3. убираем временный .ogg ─────────────────────────────
    ogg_path.unlink(missing_ok=True)

    # ── 4. возвращаем относительный путь ──────────────────────
    # Получаем относительный путь от корня проекта
    relative_path = wav_path.relative_to(RECORDS_DIR.parent)
    return str(relative_path)
