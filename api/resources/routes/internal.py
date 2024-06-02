from fastapi import APIRouter, Depends
import json
from api.domain.models.experience import Experience
from api.resources.services.experience import ExperienceService
from api.resources.routes.token import get_token

FILEPATH = 'tests/data/data.json'

def build_router(experience_service: ExperienceService) -> APIRouter:  # noqa: D103
    router = APIRouter()
    @router.post('/experiences')
    async def internal_create_experiences(token: str = Depends(get_token)):
        data = json.load(open(FILEPATH))
        for element in data:
            obj = Experience(**element)
            await experience_service.save(obj)

    return router
