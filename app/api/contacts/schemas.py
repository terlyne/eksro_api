from typing import Annotated
import uuid
from datetime import date

from pydantic import BaseModel, Field


class ContactBase(BaseModel):
    # Контактный email
    email: Annotated[str, Field(max_length=320)] | None = None
    # Контактный номер телефона
    phone: Annotated[str, Field(max_length=40)]
    # Адрес организации
    address: Annotated[str, Field(max_length=500)] | None = None
    # ВК группа ссылка
    vk_group: Annotated[str, Field(max_length=50)] | None = None
    # ТГ канал ссылка
    tg_channel: Annotated[str, Field(max_length=500)] | None = None
    # Дисциплина ответственного лица
    discipline: Annotated[str, Field(max_length=20)] | None = None
    # Фотография ответственного лица
    image_url: Annotated[str, Field(max_length=500)] | None = None
    # Режим и график работы
    work_hours: Annotated[str, Field(max_length=50)] | None = None
    # Дата создания организации
    date_of_created: date | None = None
    # Полное наименование образовательной организации
    full_name: Annotated[str, Field(max_length=500)] | None = None
    # Сокращенное наименование организации
    short_name: Annotated[str, Field(max_length=200)] | None = None
    # Учредитель образовательной организации
    organization_founder: Annotated[str, Field(max_length=50)] | None = None


class ContactCreate(ContactBase):
    pass


class ContactUpdate(ContactBase):
    email: Annotated[str | None, Field(max_length=320, default=None)]
    phone: Annotated[str | None, Field(max_length=40, default=None)]
    address: Annotated[str | None, Field(max_length=50, default=None)]
    vk_group: Annotated[str | None, Field(max_length=500, default=None)]
    tg_channel: Annotated[str | None, Field(max_length=500, default=None)]
    discipline: Annotated[str | None, Field(max_length=20, default=None)]
    image_url: Annotated[str | None, Field(max_length=500, default=None)]
    work_hours: Annotated[str | None, Field(max_length=500, default=None)]
    date_of_created: date | None = None
    full_name: Annotated[str | None, Field(max_length=500, default=None)]
    short_name: Annotated[str | None, Field(max_length=200, default=None)]
    organization_founder: Annotated[str | None, Field(max_length=500, default=None)]


class ContactResponse(ContactBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
