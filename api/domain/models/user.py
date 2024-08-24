import uuid

from pydantic import Field

from api.domain.models.base import Base


class User(Base):
    name: str = Field(...)
    email: str = Field(...)
    phone: str = Field(...)
    salt: uuid.UUID = Field(default_factory=uuid.uuid4)
    password: str = Field(...)
