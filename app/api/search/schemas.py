import uuid
from datetime import date

from pydantic import BaseModel


class NewsResponseSearch(BaseModel):
    id: uuid.UUID
    image_url: str
    min_text: str
    news_date: date


class SearchResult(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    entity_type: str
    url: str | None = None
