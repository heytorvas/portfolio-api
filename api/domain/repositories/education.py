from motor.motor_asyncio import AsyncIOMotorClient

from api.domain.models.education import Education
from api.domain.repositories.base import BaseRepository


class EducationRepository(BaseRepository):
    """Repository class for education context."""

    def __init__(self, client: AsyncIOMotorClient, collection: str) -> None:
        super().__init__(client, collection)

    model = Education
