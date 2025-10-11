from typing import Annotated
import uuid

from pydantic import BaseModel, Field


class SiteImageBase(BaseModel):
    # Название
    name: Annotated[str, Field(max_length=100)]
    # URL изображения
    image_url: Annotated[str, Field(max_length=500)]


class SiteImageCreate(SiteImageBase):
    pass


class SiteImageUpdate(SiteImageBase):
    name: Annotated[str | None, Field(max_length=10, default=None)]
    image_url: Annotated[str | None, Field(max_length=500, default=None)]


class SiteImageResponse(SiteImageBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
