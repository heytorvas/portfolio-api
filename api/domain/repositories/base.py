from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from api.exceptions import ObjectNotFoundError

if TYPE_CHECKING:
    import uuid

    from bson.typings import _DocumentType
    from motor.motor_asyncio import AsyncIOMotorClient
    from pydantic import BaseModel
    from pymongo.results import InsertOneResult


class BaseRepository:
    """Base class for repositories."""

    model: BaseModel = None

    def __init__(self, client: AsyncIOMotorClient, collection: str) -> None:
        self.client = client
        self.collection = collection
        self.object_identifier = "_id"

    async def save(self, object: model) -> InsertOneResult:
        """Save object at database collection."""
        return await self.client.insert_one(self.collection,
                                            object.dict(by_alias=True))

    async def find(self, query: Optional[dict] = None) -> list[model]:
        """Retrieve all documents at database collection."""
        response = await self.client.find(self.collection, query=query)
        if not response:
            return []
        return [self.model(**obj) for obj in response]

    async def find_one(self, object_id: uuid.UUID) -> model:
        """Return object found through search by id at database collection."""
        response = await self.client.find_one(
            self.collection, {self.object_identifier: object_id})
        if not response:
            raise ObjectNotFoundError(self.model.__name__)
        return self.model(**response)

    async def find_one_and_update(self, object_id: uuid.UUID,
                                  data: dict) -> _DocumentType:
        """Return object found through search by id and update
        at database collection.
        """
        return await self.client.find_one_and_update(
            self.collection, {self.object_identifier: object_id},
            {"$set": data})

    async def delete(self, object_id: uuid.UUID) -> None:
        """Delete document at database collection."""
        await self.find_one(object_id)
        await self.client.delete(self.collection,
                                 {self.object_identifier: object_id})
