from typing import Union
from uuid import UUID

from fastapi import APIRouter
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from api.domain.models.about import About
from api.domain.models.language import LanguageEnum
from api.resources.filters import OrderByOption, SortByOption
from api.resources.schemas.about import AboutCreateOutputSchema, \
    AboutCreateSchema, AboutSchema
from api.resources.services.about import AboutService
from api.resources.services.user import UserService


def build_router(service: AboutService,
                 user_service: UserService) -> APIRouter:
    router = APIRouter()

    @router.get("",
                response_model=Union[list[AboutSchema], list[About]],
                response_model_by_alias=False,
                status_code=HTTP_200_OK)
    async def get_about(language: LanguageEnum = None):
        sort_by = SortByOption.DATE_TO
        order_by = OrderByOption.DESC
        return await service.find(language, sort_by, order_by)

    @router.get("/{id}",
                response_model=Union[AboutSchema, About],
                response_model_by_alias=False,
                status_code=HTTP_200_OK)
    async def get_about_by_id(id: UUID, language: LanguageEnum = None):
        return await service.find_one(id, language)

    @router.post("",
                 response_model=AboutCreateOutputSchema,
                 status_code=HTTP_201_CREATED)
    async def create_about(data: AboutCreateSchema):
        await user_service.find_one(data.user)
        return await service.save(data)

    return router
