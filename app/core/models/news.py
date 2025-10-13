import uuid
from typing import TYPE_CHECKING
from datetime import date

from sqlalchemy import Text, ARRAY, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base
from core.models.mixins.id import IdMixin

if TYPE_CHECKING:
    from core.models.news_type import NewsType


class News(Base, IdMixin):
    __tablename__ = "news"

    # Заголовок новости
    title: Mapped[str] = mapped_column(Text())
    # Ссылка на новость
    news_url: Mapped[str] = mapped_column(Text())
    # Ключевые слова
    keywords: Mapped[list[str]] = mapped_column(ARRAY(Text()))
    # Изображение новости
    image_url: Mapped[str] = mapped_column(Text())
    # Минимальный текст/описание новости
    min_text: Mapped[str] = mapped_column(Text())
    # Дата новости (формата dd.mm.YYYY)
    news_date: Mapped[date]
    # Тип новости
    type_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("news_types.id"))

    type: Mapped["NewsType"] = relationship(
        back_populates="news",
    )  # Тип новости
