from sqlalchemy import String, Text, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base, SiteSection
from core.models.mixins.id import IdMixin


class DeliveredOpportunity(Base, IdMixin):
    """
    Модель для хранения доставляемых возможностей
    """

    # Подраздел секции/страницы сайта (опциональное поле, только там, где есть подразделы)
    subpage: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
    )

    __tablename__ = "delivered_opportunities"

    # Название возможности
    name: Mapped[str] = mapped_column(Text())

    # Описание возможности (может быть несколько)
    description: Mapped[str] = mapped_column(Text())

    # Целевая группа
    target_group: Mapped[str] = mapped_column(Text())

    # Ответственное лицо
    responsible_person: Mapped[str] = mapped_column(Text())

    # Фотография ответственного лица
    image_url: Mapped[str | None] = mapped_column(Text(), nullable=True)

    # Контактный номер телефона
    contact_phone: Mapped[str | None] = mapped_column(String(40), nullable=True)

    # Контактный Email адрес
    contact_email: Mapped[str | None] = mapped_column(String(320), nullable=True)
