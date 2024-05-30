from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from api.domain.models.skill import SkillEnum


class ExperienceDetail(BaseModel):
    """Experience detail model."""

    role: str = Field(...)
    project: str = Field(...)
    description: str = Field(...)


class Experience(BaseModel):
    """Experience model."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, alias='_id')
    company: str = Field(...)
    date_from: str = Field(...)
    date_to: Optional[str] = Field(...)
    stack: list[SkillEnum] = Field(...)
    details: list[ExperienceDetail] = Field(...)

    class Config:  # noqa: D106
        arbitrary_types_allowed = True
        populate_by_name = True
