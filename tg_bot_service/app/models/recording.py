from sqlalchemy import DateTime, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import TYPE_CHECKING
from app.models.base import Base
from app.common.utils import utc_plus_3


if TYPE_CHECKING:
    pass


class Recording(Base):
    __tablename__ = "recording"

    recording_session_id: Mapped[int] = mapped_column(
        ForeignKey("recording_session.id")
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    word_id: Mapped[int] = mapped_column(ForeignKey("words.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_plus_3
    )
    file_path: Mapped[str] = mapped_column(String, default="")

    user: Mapped["User"] = relationship(back_populates="recordings")
    recording_sessions: Mapped["RecordingSession"] = relationship(
        back_populates="recordings"
    )
    word: Mapped["Word"] = relationship(
        back_populates="recordings",
    )
