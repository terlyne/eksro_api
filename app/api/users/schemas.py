from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class UserResponse(BaseModel):
    email: EmailStr
    username: str
    role: str


class UserResponseForAdmin(UserResponse):
    is_active: bool


class UserUpdate(BaseModel):
    email: Annotated[EmailStr, Field(max_length=320)] | None = None
    username: Annotated[str, Field(min_length=3, max_length=20)] | None = None
