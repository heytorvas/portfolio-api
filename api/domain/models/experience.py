from __future__ import annotations

import uuid
from datetime import date, datetime, time, timezone
from typing import Union

from pydantic import BaseModel, Field, field_validator, model_validator

from api.domain.models.language import LanguageFields
from api.domain.models.skill import SkillEnum


class ExperienceDetail(BaseModel):
    """Experience detail model."""

    role: LanguageFields = Field(...)
    project: LanguageFields = Field(...)
    description: list[LanguageFields] = Field(...)


class Experience(BaseModel):
    """Experience model."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, alias='_id')
    company: str = Field(...)
    date_from: Union[str, date] = Field(...)
    date_to: Union[str, date, None] = Field(...)
    stack: list[SkillEnum] = Field(...)
    details: list[ExperienceDetail] = Field(...)

    @field_validator('date_from', 'date_to')
    def string_to_date_validator(cls, value: Union[str, date]) -> object:
        """Convert string to date object."""
        if isinstance(value, str):
            date_obj = datetime.strptime(
                f'{value}-01', '%Y-%m-%d').replace(tzinfo=timezone.utc).date()
            return datetime.combine(date_obj, time.min)
        return value

    @model_validator(mode="after")
    def date_order_validator(self) -> object:
        """Validate dates attributes values."""
        if self.date_to is not None and isinstance(self.date_from, date):
            if self.date_from >= self.date_to:
                raise ValueError(
                    'Initial date cannot be greater than final date')
            return self
        return self

    class Config:  # noqa: D106
        arbitrary_types_allowed = True
        populate_by_name = True
