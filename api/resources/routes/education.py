from typing import Union
from uuid import UUID

from fastapi import APIRouter
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from api.domain.models.education import Education
from api.domain.models.language import LanguageEnum
from api.resources.filters import OrderByOption, SortByOption
from api.resources.schemas.education import EducationCreateOutputSchema, \
    EducationCreateSchema, EducationSchema
from api.resources.services.education import EducationService
from api.resources.services.user import UserService


def builder_router(service: EducationService,
                   user_service: UserService) -> APIRouter:
    router = APIRouter()

    @router.get(
        "",
        response_model=Union[list[EducationSchema], list[Education]],
        response_model_by_alias=False,
        status_code=HTTP_200_OK,
    )
    async def get_educations(language: LanguageEnum = None,
                             sort_by: SortByOption = SortByOption.DATE_TO,
                             order_by: OrderByOption = OrderByOption.DESC):
        return await service.find(language, sort_by, order_by)

    @router.get(
        "/{id}",
        response_model=Union[EducationSchema, Education],
        response_model_by_alias=False,
        status_code=HTTP_200_OK,
    )
    async def get_education_by_id(id: UUID, language: LanguageEnum = None):
        return await service.find_one(id, language)

    @router.post("",
                 response_model=EducationCreateOutputSchema,
                 status_code=HTTP_201_CREATED)
    async def create_education(data: EducationCreateSchema):
        await user_service.find_one(data.user)
        return await service.save(data)

    return router
