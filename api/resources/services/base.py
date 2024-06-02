from uuid import UUID

from api.domain.repositories.base import BaseRepository



class BaseService:
    """Base class for services."""

    def __init__(self, repository: BaseRepository) -> None:
        self.repository = repository

    async def find_one(self, object_id: UUID) -> dict:
        """Retrieve a document from database collection."""
        return await self.repository.find_one(object_id)

    async def save(self, data) -> dict:
        """Save document at database collection."""
        object_id = await self.repository.save(data)
        return await self.find_one(object_id.inserted_id)

    async def find(self) -> list:
        """Retrieve all documents from database collection."""
        return await self.repository.find()

    async def find_one_and_update(self, object_id: UUID, data: dict) -> dict:
        """Retrieve an document and update at database collection."""
        return await self.repository.find_one_and_update(object_id, data)

    async def delete(self, object_id: UUID) -> None:
        """Delete an document at database collection."""
        await self.repository.delete(object_id)
