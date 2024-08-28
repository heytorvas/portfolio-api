from typing import Union
from uuid import UUID

from fastapi import APIRouter, status
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from api.domain.models.about import About
from api.domain.models.education import Education
from api.domain.models.experience import Experience
from api.domain.models.language import LanguageEnum
from api.resources.filters import OrderByOption, SortByOption
from api.resources.schemas.about import AboutSchema
from api.resources.schemas.education import EducationSchema
from api.resources.schemas.experience import ExperienceSchema
from api.resources.schemas.user import UserCreateSchema, UserSchema
from api.resources.services.about import AboutService
from api.resources.services.education import EducationService
from api.resources.services.experience import ExperienceService
from api.resources.services.user import UserService


def build_router(service: UserService, experience_service: ExperienceService,
                 education_service: EducationService,
                 about_service: AboutService) -> APIRouter:
    router = APIRouter()

    @router.post(
        "",
        response_model=UserSchema,
        response_model_by_alias=False,
        status_code=HTTP_201_CREATED,
    )
    async def create_user(data: UserCreateSchema):
        return await service.save(data)

    @router.get(
        "",
        response_model=list[UserSchema],
        response_model_by_alias=False,
        status_code=HTTP_200_OK,
    )
    async def get_users():
        return await service.find(language=None,
                                  sort_by=SortByOption.DATE_TO,
                                  order_by=OrderByOption.DESC)

    @router.get(
        "/{id}",
        response_model=UserSchema,
        response_model_by_alias=False,
        status_code=HTTP_200_OK,
    )
    async def get_user_by_id(id: UUID):
        return await service.find_one(id)

    @router.get("/{id}/experiences",
                status_code=status.HTTP_200_OK,
                response_model=Union[list[ExperienceSchema], list[Experience]],
                response_model_by_alias=False)
    async def get_experiences_by_user(
            id: UUID,
            language: LanguageEnum = None,
            sort_by: SortByOption = SortByOption.DATE_TO,
            order_by: OrderByOption = OrderByOption.DESC):
        user = await service.find_one(id, language)
        return await experience_service.find_by_user(user.id, language,
                                                     sort_by, order_by)

    @router.get("/{id}/educations",
                response_model=Union[list[EducationSchema], list[Education]],
                response_model_by_alias=False,
                status_code=HTTP_200_OK)
    async def get_educations_by_user(
            id: UUID,
            language: LanguageEnum = None,
            sort_by: SortByOption = SortByOption.DATE_TO,
            order_by: OrderByOption = OrderByOption.DESC):
        user = await service.find_one(id, language)
        return await education_service.find_by_user(user.id, language, sort_by,
                                                    order_by)

    @router.get("/{id}/about",
                response_model=Union[AboutSchema, About],
                response_model_by_alias=False,
                status_code=HTTP_200_OK)
    async def get_about_by_user(id: UUID, language: LanguageEnum = None):
        user = await service.find_one(id, language)
        response = await about_service.find_by_user(user.id, language,
                                                    SortByOption.DATE_TO,
                                                    OrderByOption.DESC)
        return response[0]

    return router
