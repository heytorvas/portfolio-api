from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, status

from api.domain.models.experience import Experience
from api.resources.services.experience import ExperienceService


def build_router(service: ExperienceService) -> APIRouter:  # noqa: D103
    router = APIRouter()

    @router.get('',
                status_code=status.HTTP_200_OK,
                response_model=Optional[List[Experience]],
                response_model_by_alias=False)
    async def get_experiences():
        return await service.find()

    @router.get('/{id}',
                response_model=Experience,
                response_model_by_alias=False)
    async def get_experience_by_id(id: UUID):
        return await service.find_one(id)

    @router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
    async def delete_experience_by_id(id: UUID):
        await service.delete(id)

    @router.post('',
                 status_code=status.HTTP_201_CREATED,
                 response_model=Experience,
                 response_model_by_alias=False)
    async def create_experience(data: Experience):
        return await service.save(data)

    return router
