from uuid import UUID

from fastapi import APIRouter
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from api.domain.models.language import LanguageEnum
from api.resources.schemas.user import UserCreateSchema, UserSchema
from api.resources.services.education import EducationService
from api.resources.services.experience import ExperienceService
from api.resources.services.user import UserService


def build_router(
    service: UserService,
    experience_service: ExperienceService,
    education_service: EducationService,
) -> APIRouter:
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
        return await service.find()

    @router.get(
        "/{id}",
        response_model=UserSchema,
        response_model_by_alias=False,
        status_code=HTTP_200_OK,
    )
    async def get_user_by_id(id: UUID):
        return await service.find_one(id)

    @router.get("/{id}/experiences")
    async def get_experiences_by_user(id: UUID, language: LanguageEnum = None):
        user = await service.find_one(id, language)
        if user:
            return await experience_service.find_by_user(user.id, language)
        return None

    @router.get("/{id}/educations")
    async def get_educations_by_user(id: UUID, language: LanguageEnum = None):
        user = await service.find_one(id, language)
        if user:
            return await education_service.find_by_user(user.id, language)
        return None

    return router
