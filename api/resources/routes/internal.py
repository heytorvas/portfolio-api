import json
from pathlib import Path
from fastapi import APIRouter, Depends

from api.domain.models.experience import Experience
from api.resources.routes.token import get_token
from api.resources.services.experience import ExperienceService

FILEPATH = 'tests/data/experiences.json'



def build_router( # noqa: D103
        experience_service: ExperienceService) -> APIRouter:  
    router = APIRouter()

    @router.post('/experiences')
    async def internal_create_experiences(token: str = Depends(get_token)):
        with Path.open(FILEPATH) as file:
            data = json.load(file)
        for element in data:
            obj = Experience(**element)
            await experience_service.save(obj)

    return router
