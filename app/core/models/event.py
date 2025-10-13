from datetime import datetime

from sqlalchemy import Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base
from core.models.mixins.id import IdMixin


class Event(Base, IdMixin):
    # Заголовок/название мероприятия
    title: Mapped[str] = mapped_column(Text())
    # Описание мероприятия
    description: Mapped[str] = mapped_column(
        Text()
    )  # Описание мероприятия (не в формате HTML!)
    # Дата в формате dd.mm.YYYY hh:mm
    event_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    # Изображение мероприятия
    image_url: Mapped[str] = mapped_column(Text())
    # Активно ли мероприятие
    is_active: Mapped[bool] = mapped_column(
        default=True,
        server_default="true",
    )
    # Локация
    location: Mapped[str | None] = mapped_column(
        Text(),
        nullable=True,
    )  # Место проведения
