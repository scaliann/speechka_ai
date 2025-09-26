from datetime import datetime, timedelta, timezone
from pathlib import Path


def utc_plus_3() -> datetime:
    """Возвращает текущее время + 3 ч, привязанное к UTC+3."""
    return datetime.now(timezone.utc) + timedelta(hours=3)


def progress_bar(
    done: int,
    total: int,
    width: int = 10,
) -> str:
    if total <= 0:
        return "—"
    filled = int(width * done / total)
    return "▰" * filled + "▱" * (width - filled) + f" {done} из {total}"


def get_report_path(
    diagnosis: str,
) -> Path:

    BASE_DIR = Path(__file__).parent.parent
    PDF_PATH = BASE_DIR / f"media/files/{diagnosis}.pdf"

    return PDF_PATH
