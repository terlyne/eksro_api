from typing import Annotated
import uuid

from pydantic import BaseModel, Field


class ParticipantBase(BaseModel):
    # Имя
    first_name: Annotated[str, Field(max_length=10)]
    # Фамилия
    last_name: Annotated[str, Field(max_length=100)]
    # Фотография участника (опционально)
    image_url: Annotated[str, Field(max_length=500)] | None = None


class ParticipantCreate(ParticipantBase):
    pass


class ParticipantUpdate(ParticipantBase):
    first_name: Annotated[str | None, Field(max_length=10, default=None)]
    last_name: Annotated[str | None, Field(max_length=10, default=None)]
    image_url: Annotated[str | None, Field(max_length=500, default=None)]


class ParticipantResponse(ParticipantBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
