from sqlalchemy import String

from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class TongueTwister(Base):
    __tablename__ = "tongue_twister"

    text: Mapped[str] = mapped_column(String, unique=True)
