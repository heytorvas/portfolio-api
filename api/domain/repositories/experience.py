from motor.motor_asyncio import AsyncIOMotorClient

from api.domain.models.experience import Experience
from api.domain.repositories.base import BaseRepository


class ExperienceRepository(BaseRepository):
    """Repository class for experience context."""

    def __init__(self, client: AsyncIOMotorClient, collection: str) -> None:
        super().__init__(client, collection)

    model = Experience
