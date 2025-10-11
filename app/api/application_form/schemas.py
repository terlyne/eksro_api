from typing import Annotated
import uuid

from pydantic import BaseModel, Field


class ApplicationFormBase(BaseModel):
    # Тип заявки
    application_type: Annotated[str, Field(max_length=100)]
    # Имя
    first_name: Annotated[str, Field(max_length=10)]
    # Фамилия
    last_name: Annotated[str, Field(max_length=10)] | None = None
    # Номер телефона
    phone: Annotated[str, Field(max_length=40)] | None = None
    # Адрес эл. почты
    email: Annotated[str, Field(max_length=320)]
    # Текст заявки
    text: Annotated[str, Field(max_length=1000)] | None = None
    # Флаг, отвечающий на вопрос: обработана ли заявка
    is_processed: bool = False


class ApplicationFormCreate(ApplicationFormBase):
    pass


class ApplicationFormUpdate(ApplicationFormBase):
    application_type: Annotated[str | None, Field(max_length=100, default=None)]
    first_name: Annotated[str | None, Field(max_length=100, default=None)]
    last_name: Annotated[str | None, Field(max_length=100, default=None)]
    phone: Annotated[str | None, Field(max_length=40, default=None)]
    email: Annotated[str | None, Field(max_length=320, default=None)]
    text: Annotated[str | None, Field(max_length=100, default=None)]
    is_processed: bool | None = None


class ApplicationFormResponse(ApplicationFormBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
