from sqlalchemy import String

from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Training(Base):
    __tablename__ = "training"

    text: Mapped[str] = mapped_column(String, unique=True)
