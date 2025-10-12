from typing import Annotated
import uuid

from pydantic import BaseModel, Field


class DocumentBase(BaseModel):
    # Тип страницы, на которой отображаются документы (обязательное поле)
    site_section: str
    # Подраздел секции/страницы сайта (опциональное поле)
    subpage: str | None = None
    # Название/заголовок документа
    title: Annotated[str, Field(max_length=200)]
    # Сам файл документа
    file_url: Annotated[str, Field(max_length=500)]


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(DocumentBase):
    title: Annotated[str | None, Field(max_length=200, default=None)]
    file_url: Annotated[str | None, Field(max_length=500, default=None)]


class DocumentResponse(DocumentBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
