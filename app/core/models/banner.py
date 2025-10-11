from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base
from core.models.mixins.id import IdMixin


class Banner(Base, IdMixin):
    __tablename__ = "banners"

    # Заголовок
    title: Mapped[str] = mapped_column(Text, nullable=False)
    # Описание
    description: Mapped[str] = mapped_column(Text, nullable=False)
    # Активен ли баннер
    is_active: Mapped[bool] = mapped_column(default=True, server_default="true")
    # Изображение баннера
    image_url: Mapped[str] = mapped_column(Text, nullable=False)
    # Порядок отображения
    count_order: Mapped[int] = mapped_column(unique=True, nullable=False)
