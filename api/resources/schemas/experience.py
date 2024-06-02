from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

from api.domain.models.experience import Experience


class ExperienceDetailSchema(BaseModel):
    """Schema for experience detail with one language."""

    role: str = Field(...)
    project: str = Field(...)
    description: list[str] = Field(...)


class ExperienceSchema(Experience):
    """Schema for experience context."""

    details: list[ExperienceDetailSchema]

    @field_validator("date_from", "date_to")
    def parse_date(cls, value) -> str | None:
        """Format date to string with year and month."""
        return value.strftime("%Y-%m") if value else value
