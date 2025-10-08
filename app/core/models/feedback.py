from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base
from core.models.mixins.id import IdMixin


class Feedback(Base, IdMixin):
    name: Mapped[str] = mapped_column(Text())
    phone: Mapped[str] = mapped_column(String(30))
    email: Mapped[str | None] = mapped_column(String(320))
    message: Mapped[str] = mapped_column(Text())
    is_answered: Mapped[bool] = mapped_column(default=False)
    response: Mapped[str | None] = mapped_column(nullable=True)
