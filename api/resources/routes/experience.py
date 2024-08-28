from typing import Union
from uuid import UUID

from fastapi import APIRouter, status

from api.domain.models.experience import Experience
from api.domain.models.language import LanguageEnum
from api.resources.filters import OrderByOption, SortByOption
from api.resources.schemas.experience import ExperienceCreateOutputSchema, \
    ExperienceCreateSchema, ExperienceSchema
from api.resources.services.experience import ExperienceService
from api.resources.services.user import UserService


def build_router(service: ExperienceService,
                 user_service: UserService) -> APIRouter:
    router = APIRouter()

    @router.get(
        "",
        status_code=status.HTTP_200_OK,
        response_model=Union[list[ExperienceSchema], list[Experience]],
        response_model_by_alias=False,
    )
    async def get_experiences(language: LanguageEnum = None,
                              sort_by: SortByOption = SortByOption.DATE_TO,
                              order_by: OrderByOption = OrderByOption.DESC):
        return await service.find(language, sort_by, order_by)

    @router.get(
        "/{id}",
        response_model=Union[ExperienceSchema, Experience],
        response_model_by_alias=False,
    )
    async def get_experience_by_id(id: UUID, language: LanguageEnum = None):
        return await service.find_one(id, language)

    @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_experience_by_id(id: UUID):
        await service.delete(id)

    @router.post(
        "",
        status_code=status.HTTP_201_CREATED,
        response_model=ExperienceCreateOutputSchema,
        response_model_by_alias=False,
    )
    async def create_experience(data: ExperienceCreateSchema):
        await user_service.find_one(data.user)
        return await service.save(data)

    return router
