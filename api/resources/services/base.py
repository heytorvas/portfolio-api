from typing import Union
from uuid import UUID

from pydantic import BaseModel

from api.domain.models.language import LanguageEnum, LanguageFields
from api.domain.repositories.base import BaseRepository


class BaseService:
    """Base class for services."""

    def __init__(self, repository: BaseRepository) -> None:
        self.repository = repository

    model = None
    schema = None

    @staticmethod
    def __get_attributes_with_language_type(model: BaseModel) -> list:
        model_fields = model.model_fields
        fields = []
        for field in model_fields:
            try:
                if model_fields[
                        field].annotation.__qualname__ == LanguageFields.__qualname__:
                    fields.append(field)
            except AttributeError:
                pass
        return fields

    def __create_schema_from_model(self, data: BaseModel,
                                   language: LanguageEnum):
        model_dict = data.model_dump()
        model_fields = self.__get_attributes_with_language_type(data)
        for field in model_fields:
            model_dict[field] = model_dict[field][language.value]
        return self.schema(**model_dict)

    def __get_by_language(
            self, data: Union[list[BaseModel], BaseModel],
            language: LanguageEnum) -> Union[list[BaseModel], BaseModel]:
        if isinstance(data, list):
            return [
                self.__create_schema_from_model(element, language)
                for element in data
            ]
        return self.__create_schema_from_model(data, language)

    async def find_one(self,
                       object_id: UUID,
                       language: LanguageEnum = None) -> BaseModel:
        """Retrieve a document from database collection."""
        data = await self.repository.find_one(object_id)
        if language:
            return self.__get_by_language(data, language)
        return data

    async def save(self, data) -> dict:
        """Save document at database collection."""
        object_id = await self.repository.save(self.model(**data.model_dump()))
        return await self.repository.find_one(object_id=object_id.inserted_id)

    async def find(self, language: LanguageEnum = None) -> list:
        """Retrieve all documents from database collection."""
        data = await self.repository.find()
        if language:
            return self.__get_by_language(data, language)
        return data

    async def find_by_user(self, user: UUID, language: LanguageEnum) -> list:
        """Retrieve all users' documents from database collection."""
        data = await self.repository.find({"user": user})
        if language:
            return self.__get_by_language(data, language)
        return data

    async def find_one_and_update(self, object_id: UUID, data: dict) -> dict:
        """Retrieve an document and update at database collection."""
        return await self.repository.find_one_and_update(object_id, data)

    async def delete(self, object_id: UUID) -> None:
        """Delete an document at database collection."""
        await self.repository.delete(object_id)
