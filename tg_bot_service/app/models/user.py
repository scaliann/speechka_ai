import datetime as dt
from sqlalchemy import DateTime, String, BigInteger, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timedelta, timezone
from app.common.utils import utc_plus_3

from app.base import Base


class User(Base):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    agreed_to_terms: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_plus_3
    )
    sessions: Mapped[list["RecordingSession"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    recordings: Mapped[list["Recording"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
