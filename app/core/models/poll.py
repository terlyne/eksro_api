from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base
from core.models.mixins.id import IdMixin

if TYPE_CHECKING:
    from core.models.poll_answer import PollAnswer


class Poll(Base, IdMixin):
    # Тема опроса
    theme: Mapped[str] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(default=True, server_default="true")

    answers: Mapped[list["PollAnswer"]] = relationship(
        back_populates="poll",
        cascade="all, delete-orphan",
    )
