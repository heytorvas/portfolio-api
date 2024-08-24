from datetime import date
from typing import Union
from uuid import UUID

from pydantic import BaseModel, Field

from api.domain.models.base import BaseWithDate
from api.domain.models.language import LanguageFields
from api.domain.models.skill import SkillEnum


class ExperienceDetail(BaseModel):
    """Experience detail model."""

    role: LanguageFields = Field(...)
    project: LanguageFields = Field(...)
    description: list[LanguageFields] = Field(...)


class Experience(BaseWithDate):
    user: UUID = Field(...)
    date_to: Union[str, date, None] = Field(...)
    company: str = Field(...)
    stack: list[SkillEnum] = Field(...)
    details: list[ExperienceDetail] = Field(...)

    class Config:
        use_enum_values = True
