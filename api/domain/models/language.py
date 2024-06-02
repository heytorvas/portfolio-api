from enum import Enum

from pydantic import BaseModel, Field


class LanguageFields(BaseModel):
    en: str = Field(...)
    pt: str = Field(...)


class LanguageEnum(str, Enum):
    ENGLISH = "en"
    PORTUGUESE = "pt"
