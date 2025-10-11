from typing import TYPE_CHECKING

from sqlalchemy import String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base, SiteSection
from core.models.mixins.id import IdMixin


if TYPE_CHECKING:
    from core.models.subscriber import Subscriber
    from core.models.news import News


class NewsType(Base, IdMixin):
    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum")
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
    )

    __tablename__ = "news_types"
    # Тип новости
    type: Mapped[str] = mapped_column(String(100))
    subscribers: Mapped[list["Subscriber"]] = relationship(back_populates="type")
    news: Mapped[list["News"]] = relationship(back_populates="type")
