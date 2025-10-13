from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base
from core.models.mixins.id import IdMixin


class Manager(Base, IdMixin):
    __tablename__ = "managers"

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
