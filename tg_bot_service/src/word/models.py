import datetime

from sqlalchemy import String

from src.models import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


def utc_plus_3() -> datetime:
    """Возвращает текущее время + 3 ч, привязанное к UTC+3."""
    return datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=3)


class Word(Base):
    __tablename__ = "words"

    text: Mapped[str] = mapped_column(String, unique=True)

    recordings: Mapped[list["Recording"]] = relationship(
        back_populates="word", cascade="all, delete-orphan"
    )
