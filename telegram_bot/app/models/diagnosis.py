import datetime as dt
from sqlalchemy import DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.utils import utc_plus_3
from app.models.base import Base

from app.common.enums import DiagnosisResult


class Diagnosis(Base):
    __tablename__ = "diagnosis"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    recording_session_id: Mapped[int] = mapped_column(
        ForeignKey("recording_session.id")
    )
    diagnosis: Mapped[DiagnosisResult] = mapped_column(
        Enum(DiagnosisResult),
    )
    results: Mapped[str] = mapped_column()
    finished_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), default=utc_plus_3
    )
