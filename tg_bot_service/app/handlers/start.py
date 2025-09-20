from pathlib import Path

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from app.content.start_command_text import start_command_text
from app.keyboards.menu import build_ikb_open_menu

router = Router()

START_IMAGE_PATH = (
    Path(__file__).resolve().parent.parent / "media" / "images" / "start_image.png"
)


@router.message(CommandStart())
async def command_start(message: Message):
    photo = FSInputFile(START_IMAGE_PATH)
    await message.answer_photo(
        photo=FSInputFile(START_IMAGE_PATH),
        caption=start_command_text,
        reply_markup=build_ikb_open_menu(),
    )
