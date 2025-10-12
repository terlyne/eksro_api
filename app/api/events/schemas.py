from typing import Annotated
import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class EventBase(BaseModel):
    # Заголовок/название мероприятия
    title: Annotated[str, Field(max_length=200)]
    # Описание мероприятия
    description: Annotated[str, Field(max_length=1000)]
    # Дата в формате dd.mm.YYYY hh:mm
    event_date: datetime | None = None
    # Изображение мероприятия
    image_url: Annotated[str, Field(max_length=500)]
    # Активно ли мероприятие
    is_active: bool = True
    # Локация
    location: Annotated[str, Field(max_length=200)] | None = None


class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    title: Annotated[str | None, Field(max_length=200, default=None)]
    description: Annotated[str | None, Field(max_length=100, default=None)]
    event_date: datetime | None = None
    image_url: Annotated[str | None, Field(max_length=500, default=None)]
    is_active: bool | None = None
    location: Annotated[str | None, Field(max_length=200, default=None)]


class EventResponse(EventBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
