from typing import Annotated
import uuid
from datetime import date

from pydantic import BaseModel, Field


class NewsBase(BaseModel):
    # Заголовок новости
    title: Annotated[str, Field(max_length=200)]
    # Ссылка на новость
    news_url: Annotated[str, Field(max_length=500)]
    # Ключевые слова
    keywords: list[str]
    # Изображение новости
    image_url: Annotated[str, Field(max_length=500)]
    # Минимальный текст/описание новости
    min_text: Annotated[str, Field(max_length=1000)]
    # Дата новости (формата dd.mm.YYYY)
    news_date: date
    # Тип новости
    type_id: uuid.UUID


class NewsFullResponse(NewsBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class NewsPreviewResponse(BaseModel):
    id: uuid.UUID
    image_url: str
    min_text: str


class NewsTypeBase(BaseModel):
    type: Annotated[str, Field(max_length=100)]


class NewsTypeResponse(NewsTypeBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class NewsTypeCreate(NewsTypeBase):
    pass
