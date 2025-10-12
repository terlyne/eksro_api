from typing import Annotated
import uuid

from pydantic import BaseModel, Field


class FeedbackBase(BaseModel):
    # Имя
    name: Annotated[str, Field(max_length=10)]
    # Номер телефона (опционально скорее всего)
    phone: Annotated[str, Field(max_length=30)] | None = None
    # Адрес эл. почты
    email: Annotated[str, Field(max_length=320)] | None = None
    # Текст сообщения
    message: Annotated[str, Field(max_length=100)]
    # Ответ на сообщение
    response: Annotated[str, Field(max_length=1000)] | None = None


class FeedbackCreate(FeedbackBase):
    pass


class FeedbackUpdate(FeedbackBase):
    name: Annotated[str | None, Field(max_length=10, default=None)]
    phone: Annotated[str | None, Field(max_length=30, default=None)]
    email: Annotated[str | None, Field(max_length=320, default=None)]
    message: Annotated[str | None, Field(max_length=100, default=None)]
    response: Annotated[str | None, Field(max_length=100, default=None)]


class FeedbackResponse(FeedbackBase):
    id: uuid.UUID
    is_answered: bool

    class Config:
        from_attributes = True


class FeedbackAnswer(BaseModel):
    response: Annotated[str, Field(max_length=100)]
