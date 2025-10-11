import uuid
from typing import TYPE_CHECKING
from datetime import date, datetime, timezone

from sqlalchemy import String, func, Date, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base, SiteSection
from core.models.mixins.id import IdMixin


if TYPE_CHECKING:
    from core.models.news_type import NewsType


class Subscriber(Base, IdMixin):
    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum")
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
    )

    email: Mapped[str] = mapped_column(String(320))
    subscribed_at: Mapped[date] = mapped_column(
        Date,
        server_default=func.current_date(),
        default=datetime.now(timezone.utc).date(),
    )
    is_confirmed: Mapped[bool] = mapped_column(default=False, server_default="false")
    type_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("news_types.id"))

    type: Mapped["NewsType"] = relationship(
        back_populates="subscribers",
    )
