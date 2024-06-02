from enum import Enum

from pydantic import BaseModel, Field


class LanguageFields(BaseModel):
    """Model to persist field in multiple languages."""

    en: str = Field(...)
    pt: str = Field(...)


class LanguageEnum(str, Enum):
    """Enum for language options."""

    ENGLISH = "en"
    PORTUGUESE = "pt"
