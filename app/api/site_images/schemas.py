import uuid

from pydantic import BaseModel


class SiteImageBase(BaseModel):
    name: str
    image_url: str


class SiteImageResponse(SiteImageBase):
    id: uuid.UUID
