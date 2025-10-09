import uuid
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    id: uuid.UUID
    email: Annotated[EmailStr, Field(max_length=320)]
    username: Annotated[str, Field(min_length=3, max_length=20)]
    role: str


class UserResponse(UserBase):
    pass


class UserUpdate(BaseModel):
    email: Annotated[EmailStr, Field(max_length=320)] | None = None
    username: Annotated[str, Field(min_length=3, max_length=20)] | None = None
