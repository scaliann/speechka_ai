import datetime as dt
from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.models.base import Base

from app.common.enums import SessionStatus
from app.common.utils import utc_plus_3


class RecordingSession(Base):
    __tablename__ = "recording_session"
    __table_args__ = (
        UniqueConstraint("user_id", "session_number", name="uq_user_session_number"),
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    session_number: Mapped[int] = mapped_column(ForeignKey("recording_session.id"))
    status: Mapped[SessionStatus] = mapped_column(
        Enum(SessionStatus),
        default=SessionStatus.active,
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_plus_3
    )
    finished_at: Mapped[dt.datetime | None]

    user: Mapped["User"] = relationship(
        back_populates="recording_sessions",
    )
    recordings: Mapped[list["Recording"]] = relationship(
        back_populates="recording_sessions",
        cascade="all, delete-orphan",
    )
