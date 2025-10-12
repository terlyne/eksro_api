from typing import Annotated
import uuid

from pydantic import BaseModel, Field


class ManagerBase(BaseModel):
    # Тип страницы, на которой отображаются контакты (обязательное поле)
    site_section: str
    # Подраздел секции/страницы сайта (опциональное поле)
    subpage: str | None = None
    # Фотография члена руководства
    image_url: Annotated[str, Field(max_length=500)] | None = None
    # ФИО
    full_name: Annotated[str, Field(max_length=200)]
    # Должность
    position: Annotated[str, Field(max_length=200)]
    # Контактный номер телефона
    phone: Annotated[str, Field(max_length=40)] | None = None
    # Контактный Email адрес
    email: Annotated[str, Field(max_length=320)] | None = None


class ManagerCreate(ManagerBase):
    pass


class ManagerUpdate(ManagerBase):
    image_url: Annotated[str | None, Field(max_length=500, default=None)]
    full_name: Annotated[str | None, Field(max_length=20, default=None)]
    position: Annotated[str | None, Field(max_length=200, default=None)]
    phone: Annotated[str | None, Field(max_length=40, default=None)]
    email: Annotated[str | None, Field(max_length=320, default=None)]


class ManagerResponse(ManagerBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
