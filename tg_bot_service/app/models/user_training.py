from sqlalchemy import String, ForeignKey, Boolean

from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class UserTraining(Base):
    __tablename__ = "user_training"

    training_id: Mapped[int] = mapped_column(ForeignKey("training.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    is_done: Mapped[bool] = mapped_column(Boolean, default=False)
