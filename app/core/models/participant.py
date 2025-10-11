from sqlalchemy import Text, String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base, SiteSection
from core.models.mixins.id import IdMixin


class Participant(Base, IdMixin):
    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum")
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
    )

    # Имя
    first_name: Mapped[str] = mapped_column(Text())
    # Фамилия
    last_name: Mapped[str] = mapped_column(Text())
    # Фотография участника (опционально)
    image_url: Mapped[str | None] = mapped_column(Text(), nullable=True)
