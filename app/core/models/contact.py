from datetime import date

from sqlalchemy import String, Text, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base, SiteSection
from core.models.mixins.id import IdMixin


class Contact(Base, IdMixin):
    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum")
    )

    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
    )

    phone: Mapped[str] = mapped_column(String(40))
    email: Mapped[str] = mapped_column(String(320), nullable=True)
    address: Mapped[str] = mapped_column(Text(), nullable=True)
    vk_group: Mapped[str] = mapped_column(Text(), nullable=True)  # Ссылка на группу ВК
    tg_channel: Mapped[str] = mapped_column(
        Text(),
        nullable=True,
    )  # Ссылка на канал в телеграмме
    discipline: Mapped[str] = mapped_column(
        Text(),
        nullable=True,
    )  # Название дисциплины ответственного лица
    image_url: Mapped[str] = mapped_column(
        Text(),
        nullable=True,
    )  # URL изображения ответсвенного лица
    work_hours: Mapped[str] = mapped_column(
        Text(),
        nullable=True,
    )  # Часы работы
    date_of_created: Mapped[date] = mapped_column(
        nullable=True
    )  # Дата создания организации
    full_name: Mapped[str] = mapped_column(
        Text(), nullable=True
    )  # Полное название организации
    short_name: Mapped[str] = mapped_column(
        Text(), nullable=True
    )  # Сокращенное название организации
    organization_founder: Mapped[str] = mapped_column(
        Text(), nullable=True
    )  # Учредитель-компания организации
