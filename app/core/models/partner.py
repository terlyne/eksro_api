from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base
from core.models.mixins.id import IdMixin


class Partner(Base, IdMixin):
    __tablename__ = "partners"

    # Название
    partner_name: Mapped[str] = mapped_column(Text())
    # Порядок отображения (надо валидировать, чтобы двух партнеров с одинаковым порядком не было)
    count_order: Mapped[int] = mapped_column(unique=True)
    # Сайт партнера (опционально)
    partner_url: Mapped[str | None] = mapped_column(
        Text(), nullable=True
    )  # URL сайта партнера
    # Логотип партнера
    logo_url: Mapped[str] = mapped_column(Text())
