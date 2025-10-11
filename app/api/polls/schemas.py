from typing import Annotated
import uuid

from pydantic import BaseModel, Field


class PollBase(BaseModel):
    # Тема опроса
    theme: Annotated[str, Field(max_length=100)]
    is_active: bool = True


class PollCreate(PollBase):
    pass


class PollUpdate(PollBase):
    theme: Annotated[str | None, Field(max_length=100, default=None)]
    is_active: bool | None = None


class PollResponse(PollBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class PollAnswerBase(BaseModel):
    # Текст ответа пользователя
    answer_text: Annotated[str, Field(max_length=100)]


class PollAnswerCreate(PollAnswerBase):
    pass


class PollAnswerUpdate(PollAnswerBase):
    answer_text: Annotated[str | None, Field(max_length=10, default=None)]


class PollAnswerResponse(PollAnswerBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
