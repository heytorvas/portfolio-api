from uuid import UUID

from pydantic import BaseModel, Field

from api.domain.models.about import About, Address, SocialNetwork
from api.domain.models.language import LanguageFields


class AboutSchema(About):
    id: UUID = Field()
    summary: str = Field()


class AboutCreateSchema(BaseModel):
    user: UUID = Field()
    address: Address = Field()
    social_network: SocialNetwork = Field()
    summary: LanguageFields = Field()


class AboutCreateOutputSchema(AboutCreateSchema):
    id: UUID = Field()
