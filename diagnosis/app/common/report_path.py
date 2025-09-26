from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


def get_report_path(
    diagnosis: str,
) -> Path:
    """
    Возвращает путь до pdf отчета в зависимости от диагноза.
    """
    pdf_path = BASE_DIR / f"media/files/{diagnosis}.pdf"
    return pdf_path
