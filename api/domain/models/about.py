import uuid
from typing import Optional

from pydantic import BaseModel, Field

from api.domain.models.base import Base
from api.domain.models.language import LanguageFields


class Address(BaseModel):
    city: str = Field(...)
    state: str = Field(...)
    country: str = Field(...)


class SocialNetwork(BaseModel):
    website: Optional[str] = Field()
    github: Optional[str] = Field()
    linkedin: Optional[str] = Field()


class About(Base):
    user: uuid.UUID = Field(...)
    address: Address = Field(...)
    social_network: SocialNetwork = Field(...)
    summary: LanguageFields = Field(...)
