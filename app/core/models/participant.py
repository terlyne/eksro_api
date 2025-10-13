from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base
from core.models.mixins.id import IdMixin


class Participant(Base, IdMixin):

    # Имя
    first_name: Mapped[str] = mapped_column(Text())
    # Фамилия
    last_name: Mapped[str] = mapped_column(Text())
    # Фотография участника (опционально)
    image_url: Mapped[str | None] = mapped_column(Text(), nullable=True)
