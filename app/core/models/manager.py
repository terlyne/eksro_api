from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base
from core.models.mixins.id import IdMixin


class Manager(Base, IdMixin):
    """Модель члена руководства"""

    first_name: Mapped[str] = mapped_column(Text())
    last_name: Mapped[str] = mapped_column(Text())
    patronymic: Mapped[str] = mapped_column(Text())  # Отчество
    post: Mapped[str] = mapped_column(Text())  # Занимаемая членом руководства должность
