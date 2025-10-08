from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base
from core.models.mixins.id import IdMixin


class Banner(Base, IdMixin):
    image_url: Mapped[str] = mapped_column(Text())
    title: Mapped[str] = mapped_column(Text())
    description: Mapped[str] = mapped_column(Text())
    is_active: Mapped[bool] = mapped_column(default=True, server_default="true")
    count_order: Mapped[int]  # Порядок отображения
