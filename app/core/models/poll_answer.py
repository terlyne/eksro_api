from typing import TYPE_CHECKING
import uuid

from sqlalchemy import ForeignKey, Text, String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base, SiteSection
from core.models.mixins.id import IdMixin

if TYPE_CHECKING:
    from core.models.poll import Poll


class PollAnswer(Base, IdMixin):
    __tablename__ = "poll_answers"

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum")
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
    )

    answer_text: Mapped[str] = mapped_column(Text())  # Текст ответа
    poll_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("polls.id"))

    poll: Mapped["Poll"] = relationship(back_populates="answers")
