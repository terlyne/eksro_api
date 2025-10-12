from sqlalchemy import String, Text, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base, SiteSection
from core.models.mixins.id import IdMixin


class Manager(Base, IdMixin):
    __tablename__ = "managers"

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum"), default=SiteSection.ABOUT
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
    )

    # Фотография члена руководства
    image_url: Mapped[str | None] = mapped_column(Text(), nullable=True)
    # ФИО
    full_name: Mapped[str] = mapped_column(Text())
    # Должность
    position: Mapped[str] = mapped_column(Text())
    # Контактный номер телефона
    phone: Mapped[str | None] = mapped_column(String(40), nullable=True)
    # Контактный Email адрес
    email: Mapped[str | None] = mapped_column(String(320), nullable=True)
