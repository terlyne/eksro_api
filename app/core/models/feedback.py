from sqlalchemy import String, Text, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base, SiteSection
from core.models.mixins.id import IdMixin


class Feedback(Base, IdMixin):
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
    name: Mapped[str] = mapped_column(Text())
    # Номер телефона (опционально скорее всего)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    # Адрес эл. почты
    email: Mapped[str | None] = mapped_column(String(320))
    # Текст сообщения
    message: Mapped[str] = mapped_column(Text())
    # Флаг, отвечающий на вопрос: отвечено ли
    is_answered: Mapped[bool] = mapped_column(default=False)
    # Ответ на сообщение
    response: Mapped[str | None] = mapped_column(nullable=True)
