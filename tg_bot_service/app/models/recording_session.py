import datetime as dt
from sqlalchemy import DateTime, String, BigInteger, ForeignKey, UniqueConstraint, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING
from app.base import Base

from app.common.enums import SessionStatus
from app.common.utils import utc_plus_3

if TYPE_CHECKING:
    from app.user.models import User
    from app.word.models import Word


class RecordingSession(Base):
    __tablename__ = "recording_session"
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
