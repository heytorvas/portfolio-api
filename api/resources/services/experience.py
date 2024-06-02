from __future__ import annotations

from typing import TYPE_CHECKING

from api.domain.models.experience import Experience
from api.resources.schemas.experience import ExperienceDetailSchema, \
    ExperienceSchema
from api.resources.services.base import BaseService

if TYPE_CHECKING:
    from uuid import UUID

    from api.domain.models.language import LanguageEnum


class ExperienceService(BaseService):
    """Service class for experience context."""

    @staticmethod
    def __get_by_language(data: Experience | list[Experience],
                          language: LanguageEnum) -> [ExperienceSchema]:
        if isinstance(data, Experience):
            data = [data]
        response = []
        for experience in data:
            details = []
            for detail in experience.details:
                descriptions = [
                    description.__dict__[language]
                    for description in detail.description
                ]
                details.append(
                    ExperienceDetailSchema(
                        role=detail.role.__dict__[language],
                        project=detail.project.__dict__[language],
                        description=descriptions))
            response.append(
                ExperienceSchema(id=experience.id,
                                 company=experience.company,
                                 date_from=experience.date_from,
                                 date_to=experience.date_to,
                                 stack=experience.stack,
                                 details=details))
        return response

    async def find(self, language: LanguageEnum):
        """Retrieve all documents from database collection."""
        data = await self.repository.find()
        if language:
            return self.__get_by_language(data, language)
        return data

    async def find_one(self, object_id: UUID,
                       language: LanguageEnum) -> Experience:
        """Retrieve a document from database collection."""
        data = await self.repository.find_one(object_id)
        if language:
            return self.__get_by_language(data, language)[0]
        return data
