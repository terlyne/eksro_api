from typing import Annotated
import uuid

from pydantic import BaseModel, EmailStr, Field


class FeedbackBase(BaseModel):
    name: str
    phone: Annotated[str, Field(max_length=30)]
    email: Annotated[EmailStr, Field(max_length=320)]
    message: str


class FeedbackResponse(FeedbackBase):
    id: uuid.UUID
    is_answered: bool
    response: str | None = None


class FeedbackCreate(FeedbackBase):
    pass


class FeedbackAnswer(BaseModel):
    response: str | None = None
