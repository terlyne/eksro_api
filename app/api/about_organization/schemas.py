from typing import Annotated
import uuid
from datetime import date

from pydantic import BaseModel, Field


class AboutOrganizationBase(BaseModel):
    # Заголовок (вроде статичный - Основные сведения)
    title: Annotated[str, Field(max_length=100, default="Основные сведения")]
    # Полное наименование образовательной организации
    full_name: Annotated[str, Field(max_length=500)]
    # Сокращенное наименование организации
    short_name: Annotated[str, Field(max_length=20)]
    # Дата создания образовательной организации (в формате dd.mm.YYYY)
    creation_date: date
    # Учредитель образовательной организации
    founder: Annotated[str, Field(max_length=500)]
    # Место нахождения образовательной организации
    location: Annotated[str, Field(max_length=500)]
    # Режим и график работы
    work_schedule: Annotated[str, Field(max_length=500)]
    # Контактный телефон
    contact_phone: Annotated[str, Field(max_length=40)]
    # Адрес электронной почты
    contact_email: Annotated[str, Field(max_length=320)]


class AboutOrganizationCreate(AboutOrganizationBase):
    pass


class AboutOrganizationUpdate(AboutOrganizationBase):
    title: Annotated[str | None, Field(max_length=10, default=None)]
    full_name: Annotated[str | None, Field(max_length=500, default=None)]
    short_name: Annotated[str | None, Field(max_length=20, default=None)]
    creation_date: date | None = None
    founder: Annotated[str | None, Field(max_length=500, default=None)]
    location: Annotated[str | None, Field(max_length=500, default=None)]
    work_schedule: Annotated[str | None, Field(max_length=500, default=None)]
    contact_phone: Annotated[str | None, Field(max_length=40, default=None)]
    contact_email: Annotated[str | None, Field(max_length=320, default=None)]


class AboutOrganizationResponse(AboutOrganizationBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
