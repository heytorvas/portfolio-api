from datetime import date
from typing import Union
from uuid import UUID

from pydantic import BaseModel, Field

from api.domain.models.education import Education
from api.domain.models.language import LanguageFields


class EducationSchema(Education):
    id: UUID = Field()
    degree: str = Field()
    school: str = Field()
    course: str = Field()


class EducationCreateSchema(BaseModel):
    user: UUID = Field(...)
    degree: LanguageFields = Field(...)
    school: LanguageFields = Field(...)
    course: LanguageFields = Field(...)
    date_from: Union[str, date] = Field(...)
    date_to: Union[str, date] = Field(...)


class EducationCreateOutputSchema(EducationCreateSchema):
    id: UUID = Field(...)
