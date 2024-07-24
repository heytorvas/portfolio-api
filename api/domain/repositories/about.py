from motor.motor_asyncio import AsyncIOMotorClient

from api.domain.models.about import About
from api.domain.repositories.base import BaseRepository


class AboutRepository(BaseRepository):
    """Repository class for about context."""

    def __init__(self, client: AsyncIOMotorClient, collection: str) -> None:
        super().__init__(client, collection)

    model = About
