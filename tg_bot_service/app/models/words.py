import datetime

from sqlalchemy import String

from app.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.common.utils import utc_plus_3


class Word(Base):
    __tablename__ = "words"

    text: Mapped[str] = mapped_column(String, unique=True)

    recordings: Mapped[list["Recording"]] = relationship(
        back_populates="word", cascade="all, delete-orphan"
    )
