from __future__ import annotations

from typing import TYPE_CHECKING, Union

from api.domain.models.experience import Experience
from api.resources.schemas.experience import ExperienceDetailSchema, \
    ExperienceSchema
from api.resources.services.base import BaseService

if TYPE_CHECKING:
    from uuid import UUID

    from api.domain.models.language import LanguageEnum


class ExperienceService(BaseService):
    """Service class for experience context."""

    model = Experience
    schema = ExperienceSchema

    @staticmethod
    def __get_by_language(data: Experience | list[Experience],
                          language: LanguageEnum) -> [ExperienceSchema]:
        if isinstance(data, Experience):
            data = [data]
        return [
            ExperienceSchema(
                id=experience.id,
                user=experience.user,
                company=experience.company,
                date_from=experience.date_from,
                date_to=experience.date_to,
                stack=experience.stack,
                details=[
                    ExperienceDetailSchema(
                        role=detail.role.__dict__[language],
                        project=detail.project.__dict__[language],
                        description=[
                            description.__dict__[language]
                            for description in detail.description
                        ],
                    ) for detail in experience.details
                ],
            ) for experience in data
        ]

    async def find(
        self,
        language: LanguageEnum = None
    ) -> Union[list[Experience], list[ExperienceSchema]]:
        """Retrieve all documents from database collection."""
        data = await self.repository.find()
        if language:
            return self.__get_by_language(data, language)
        return data

    async def find_one(
            self,
            object_id: UUID,
            language: LanguageEnum = None
    ) -> Union[Experience, ExperienceSchema]:
        """Retrieve a document from database collection."""
        data = await self.repository.find_one(object_id)
        if language:
            return self.__get_by_language(data, language)[0]
        return data

    async def find_by_user(self, user: UUID, language: LanguageEnum) -> list:
        """Retrieve all users' documents from database collection."""
        data = await self.repository.find({"user": user})
        if language:
            return self.__get_by_language(data, language)
        return data
