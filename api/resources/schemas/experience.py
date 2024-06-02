from pydantic import BaseModel, Field
from api.domain.models.experience import Experience

class ExperienceDetailSchema(BaseModel):
    role: str = Field(...)
    project: str = Field(...)
    description: list[str] = Field(...)


class ExperienceSchema(Experience):
    details: list[ExperienceDetailSchema]
