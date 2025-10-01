import uuid
from typing import TYPE_CHECKING
from datetime import date

from sqlalchemy import Text, String, ARRAY, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base
from core.models.mixins.id import IdMixin

if TYPE_CHECKING:
    from core.models.news_type import NewsType


class News(Base, IdMixin):
    __tablename__ = "news"

    title: Mapped[str] = mapped_column(Text())
    news_url: Mapped[str] = mapped_column(Text())  # Ссылка на новость

    # Ключевые слова для поиска внутри сайта
    keywords: Mapped[list[str]] = mapped_column(ARRAY(Text()))
    image_url: Mapped[str] = mapped_column(Text())
    min_text: Mapped[str] = mapped_column(
        Text()
    )  # Минимальный текст для отображения на главной странице
    news_date: Mapped[date]  # Дата новости
    type_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("news_types.id"))

    type: Mapped["NewsType"] = relationship(
        back_populates="news",
    )  # Тип новости
