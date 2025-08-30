import datetime as dt
from sqlalchemy import DateTime, String, BigInteger, ForeignKey, UniqueConstraint, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING
from src.models import Base
from enum import Enum as PyEnum

if TYPE_CHECKING:
    from tg_bot_service.src.user import User
    from tg_bot_service.src.word import Word


def utc_plus_3() -> datetime:
    """Возвращает текущее время + 3 ч, привязанное к UTC+3."""
    return datetime.now(timezone.utc) + timedelta(hours=3)


class SessionStatus(PyEnum):
    active = "active"
    completed = "completed"
    aborted = "aborted"


class Recording(Base):
    __tablename__ = "recordings"

    session_id: Mapped[int] = mapped_column(ForeignKey("recording_sessions.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    word_id: Mapped[int] = mapped_column(ForeignKey("words.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_plus_3
    )
    file_path: Mapped[str] = mapped_column(String, default="")

    user: Mapped["User"] = relationship(back_populates="recordings")
    session: Mapped["RecordingSession"] = relationship(back_populates="recordings")
    word: Mapped["Word"] = relationship(back_populates="recordings")


class RecordingSession(Base):
    __tablename__ = "recording_sessions"
    __table_args__ = (
        UniqueConstraint("user_id", "session_number", name="uq_user_session_number"),
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    session_number: Mapped[int]
    status: Mapped[SessionStatus] = mapped_column(
        Enum(SessionStatus),
        default=SessionStatus.active,
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_plus_3
    )
    finished_at: Mapped[dt.datetime | None]

    user: Mapped["User"] = relationship(
        back_populates="sessions",
    )
    recordings: Mapped[list["Recording"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
    )
