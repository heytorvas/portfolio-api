from uuid import UUID

from pydantic import Field

from api.domain.models.base import BaseWithDate
from api.domain.models.language import LanguageFields


class Education(BaseWithDate):
    user: UUID = Field(...)
    degree: LanguageFields = Field(...)
    school: LanguageFields = Field(...)
    course: LanguageFields = Field(...)
