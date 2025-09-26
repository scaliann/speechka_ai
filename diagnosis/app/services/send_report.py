from pathlib import Path

from aiogram import Bot
from aiogram.types import Message, FSInputFile

from app.config import settings

BOT_TOKEN = settings.telegram_bot_token
if not BOT_TOKEN:
    raise RuntimeError("Не найден BOT_TOKEN в .env")

bot = Bot(BOT_TOKEN)


async def send_pdf_report(
    chat_id: int,
    report_path: Path,
) -> Message:
    """
    Функция отвечает за формирование файла и его отправку пользователю.
    """

    report = FSInputFile(
        report_path,
        filename="Результат диагностики.pdf",
    )

    return await bot.send_document(
        chat_id=chat_id,
        document=report,
        caption=f"""
📄 Ваш отчет по проведенной диагностике готов!

❕ Напоминаем, что содержимое отчета не является диагнозом, а всего лишь предположением с дружескими советами :)
""",
    )
