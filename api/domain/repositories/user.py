from motor.motor_asyncio import AsyncIOMotorClient

from api.domain.models.user import User
from api.domain.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    """Repository class for about context."""

    def __init__(self, client: AsyncIOMotorClient, collection: str) -> None:
        super().__init__(client, collection)

    model = User
