from typing import Annotated
import uuid

from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    # Заголовок
    title: Annotated[str, Field(max_length=200)]
    # Ссылка на проект
    project_url: Annotated[str, Field(max_length=500)]
    # Ключевые слова
    keywords: list[str]
    # Минимальный текст/описание для его отображения на главной странице
    min_text: Annotated[str, Field(max_length=1000)]
    # Изображение проекта
    image_url: Annotated[str, Field(max_length=500)]
    # Тема проекта
    theme: Annotated[str, Field(max_length=25)]
    # Категория
    category: Annotated[str, Field(max_length=255)]
    # Активен ли проект
    is_active: bool = True


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    title: Annotated[str | None, Field(max_length=200, default=None)]
    project_url: Annotated[str | None, Field(max_length=500, default=None)]
    keywords: list[str] | None = None
    min_text: Annotated[str | None, Field(max_length=100, default=None)]
    image_url: Annotated[str | None, Field(max_length=500, default=None)]
    theme: Annotated[str | None, Field(max_length=255, default=None)]
    category: Annotated[str | None, Field(max_length=25, default=None)]
    is_active: bool | None = None


class ProjectResponse(ProjectBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
