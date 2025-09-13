from sqlalchemy import String

from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Word(Base):
    __tablename__ = "words"

    text: Mapped[str] = mapped_column(String, unique=True)

    recordings: Mapped[list["Recording"]] = relationship(
        back_populates="word", cascade="all, delete-orphan"
    )
