from datetime import date

from sqlalchemy import String, Text, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base, SiteSection
from core.models.mixins.id import IdMixin


class AboutOrganization(Base, IdMixin):
    """
    Модель для хранения основных сведений об образовательной организации
    """

    # Добавляем тип страницы, на котором эти контакты отображаются (обязательное поле)
    site_section: Mapped[SiteSection] = mapped_column(
        SQLEnum(SiteSection, name="sitesection_enum")
    )
    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
    )

    __tablename__ = "about_organizations"

    # Заголовок (статичный - "Основные сведения")
    title: Mapped[str] = mapped_column(Text(), default="Основные сведения")

    # Полное наименование образовательной организации
    full_name: Mapped[str] = mapped_column(Text())

    # Сокращенное наименование организации
    short_name: Mapped[str] = mapped_column(Text())

    # Дата создания образовательной организации (в формате dd.mm.YYYY)
    creation_date: Mapped[date]

    # Учредитель образовательной организации
    founder: Mapped[str] = mapped_column(Text())

    # Место нахождения образовательной организации
    location: Mapped[str] = mapped_column(Text())

    # Режим и график работы
    work_schedule: Mapped[str] = mapped_column(Text())

    # Контактный телефон
    contact_phone: Mapped[str] = mapped_column(String(40))

    # Адрес электронной почты
    contact_email: Mapped[str] = mapped_column(String(320))
