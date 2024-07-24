from datetime import date
from typing import Union
from uuid import UUID

from pydantic import BaseModel, Field

from api.domain.models.experience import Experience, ExperienceDetail
from api.domain.models.skill import SkillEnum


class ExperienceDetailSchema(BaseModel):
    """Schema for experience detail with one language."""

    role: str = Field(...)
    project: str = Field(...)
    description: list[str] = Field(...)


class ExperienceSchema(Experience):
    id: UUID = Field(...)
    details: list[ExperienceDetailSchema] = Field(...)


class ExperienceCreateSchema(BaseModel):
    user: UUID = Field(...)
    company: str = Field(...)
    stack: list[SkillEnum] = Field(...)
    details: list[ExperienceDetail] = Field(...)
    date_from: Union[str, date] = Field(...)
    date_to: Union[str, date, None] = Field(...)


class ExperienceCreateOutputSchema(ExperienceCreateSchema):
    id: UUID = Field(...)


# class ExperienceSchema(Experience):
#     """Schema for experience context."""
#
#
#     @field_validator("date_from", "date_to")
#     def parse_date(cls, value) -> str | None:
#         """Format date to string with year and month."""
