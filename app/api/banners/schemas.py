from typing import Annotated
import uuid

from pydantic import BaseModel, Field


class BannerBase(BaseModel):
    # Заголовок
    title: Annotated[str, Field(max_length=200)]
    # Описание
    description: Annotated[str, Field(max_length=200)]
    # Активен ли баннер
    is_active: bool = True
    # Изображение баннера
    image_url: Annotated[str, Field(max_length=500)]
    # Порядок отображения
    count_order: int


class BannerCreate(BannerBase):
    pass


class BannerUpdate(BannerBase):
    title: Annotated[str | None, Field(max_length=200, default=None)]
    description: Annotated[str | None, Field(max_length=100, default=None)]
    is_active: bool | None = None
    image_url: Annotated[str | None, Field(max_length=500, default=None)]
    count_order: int | None = None


class BannerResponse(BannerBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
