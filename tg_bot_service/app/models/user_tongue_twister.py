from sqlalchemy import String, ForeignKey, Boolean

from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class UserTongueTwister(Base):
    __tablename__ = "user_tongue_twister"

    tongue_twister_id: Mapped[int] = mapped_column(ForeignKey("tongue_twister.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
