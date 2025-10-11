from typing import Annotated
import uuid

from pydantic import BaseModel, Field


class PartnerBase(BaseModel):
    # Название
    partner_name: Annotated[str, Field(max_length=200)]
    # Порядок отображения (надо валидировать, чтобы двух партнеров с одинаковым порядком не было)
    count_order: int
    # Сайт партнера (опционально)
    partner_url: Annotated[str, Field(max_length=500)] | None = None
    # Логотип партнера
    logo_url: Annotated[str, Field(max_length=500)]


class PartnerCreate(PartnerBase):
    pass


class PartnerUpdate(PartnerBase):
    partner_name: Annotated[str | None, Field(max_length=20, default=None)]
    count_order: int | None = None
    partner_url: Annotated[str | None, Field(max_length=500, default=None)]
    logo_url: Annotated[str | None, Field(max_length=500, default=None)]


class PartnerResponse(PartnerBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
