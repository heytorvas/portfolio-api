from __future__ import annotations

from pydantic import BaseModel, Field

from api.domain.models.experience import Experience


class ExperienceDetailSchema(BaseModel):
    """Schema for experience detail with one language."""

    role: str = Field(...)
    project: str = Field(...)
    description: list[str] = Field(...)


class ExperienceSchema(Experience):
    """Schema for experience context."""

    details: list[ExperienceDetailSchema]
