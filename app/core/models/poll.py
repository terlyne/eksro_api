from typing import TYPE_CHECKING

from sqlalchemy import String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base, SiteSection
from core.models.mixins.id import IdMixin

if TYPE_CHECKING:
    from core.models.poll_answer import PollAnswer


class Poll(Base, IdMixin):
    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum")
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
    )

    theme: Mapped[str] = mapped_column(String(100))  # Тема опроса
    is_active: Mapped[bool] = mapped_column(default=True, server_default="true")

    answers: Mapped[list["PollAnswer"]] = relationship(
        back_populates="poll",
        cascade="all, delete-orphan",
    )
