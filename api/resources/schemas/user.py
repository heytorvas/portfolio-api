from uuid import UUID

from pydantic import BaseModel, Field

from api.domain.models.user import User


class UserSchema(User):
    id: UUID = Field(...)
    password: str = Field(..., exclude=True)
    salt: UUID = Field(..., exclude=True)


class UserCreateSchema(BaseModel):
    name: str = Field(...)
    email: str = Field(...)
    phone: str = Field(...)
    password: str = Field(...)
