from typing import Annotated
import uuid

from pydantic import BaseModel, Field


class DeliveredOpportunityBase(BaseModel):
    # Название
    name: Annotated[str, Field(max_length=200)]
    # Описание возможности/Описание возможности/ (то есть по сути список, потому что может быть несколько описаний возможностей)
    description: Annotated[str, Field(max_length=1000)]
    # Целевая группа
    target_group: Annotated[str, Field(max_length=200)]
    # Ответственное лицо
    responsible_person: Annotated[str, Field(max_length=200)]
    # Фотография отвественного лица
    image_url: str | None = None
    # Контактный номер телефона
    contact_phone: Annotated[str, Field(max_length=40)] | None = None
    # Контактный Email адрес
    contact_email: Annotated[str, Field(max_length=320)] | None = None


class DeliveredOpportunityCreate(DeliveredOpportunityBase):
    pass


class DeliveredOpportunityUpdate(DeliveredOpportunityBase):
    name: Annotated[str | None, Field(max_length=200, default=None)]
    description: Annotated[str | None, Field(max_length=100, default=None)]
    target_group: Annotated[str | None, Field(max_length=200, default=None)]
    responsible_person: Annotated[str | None, Field(max_length=200, default=None)]
    image_url: Annotated[str | None, Field(max_length=500, default=None)]
    contact_phone: Annotated[str | None, Field(max_length=40, default=None)]
    contact_email: Annotated[str | None, Field(max_length=320, default=None)]


class DeliveredOpportunityResponse(DeliveredOpportunityBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
