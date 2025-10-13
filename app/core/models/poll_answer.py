from typing import TYPE_CHECKING
import uuid

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base
from core.models.mixins.id import IdMixin

if TYPE_CHECKING:
    from core.models.poll import Poll


class PollAnswer(Base, IdMixin):
    __tablename__ = "poll_answers"

    # Текст ответа пользователя
    answer_text: Mapped[str] = mapped_column(Text())
    poll_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("polls.id"))

    poll: Mapped["Poll"] = relationship(back_populates="answers")
