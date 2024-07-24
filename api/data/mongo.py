from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union

from bson.errors import BSONError
from pymongo import ReturnDocument
from pymongo.errors import PyMongoError

from api.exceptions import DatabaseError

if TYPE_CHECKING:
    from bson.typings import _DocumentType
    from motor.motor_asyncio import AsyncIOMotorClient
    from pymongo.results import DeleteResult, InsertOneResult


class MongoDatabase:
    """Abstract connection class with MongoDB."""

    def __init__(self, client: AsyncIOMotorClient, database: str) -> None:
        self.client = client
        self.database = database

    @staticmethod
    def _query_db_error(error: Union[str, Exception]) -> DatabaseError:
        message = str(error).strip()
        return DatabaseError(message)

    async def insert_one(self, collection: str,
                         query: dict) -> InsertOneResult:
        """Insert one document at database collection."""
        try:
            db = self.client[self.database]
            coll = db[collection]
            return await coll.insert_one(query)
        except (PyMongoError, BSONError) as error:
            raise self._query_db_error(error) from error

    async def find(
        self,
        collection: str,
        query: Union[dict, None] = None,
        sort: Union[list, None] = None,
        limit: int = 100,
    ) -> Optional[_DocumentType]:
        """Retrieve a list by search at database collection."""
        try:
            if query is None:
                query = {}
            db = self.client[self.database]
            coll = db[collection]
            return [
                doc async for doc in coll.find(query, sort=sort).limit(limit)
            ]
        except (PyMongoError, BSONError) as error:
            raise self._query_db_error(error) from error

    async def find_one(
            self,
            collection: str,
            query: Union[dict, None] = None) -> Optional[_DocumentType]:
        """Retrieve only one document by search."""
        try:
            db = self.client[self.database]
            coll = db[collection]
            return await coll.find_one(query)
        except (PyMongoError, BSONError) as error:
            raise self._query_db_error(error) from error

    async def delete(self, collection: str, query: dict) -> DeleteResult:
        """Delete one document by search."""
        try:
            db = self.client[self.database]
            coll = db[collection]
            return await coll.delete_one(query)
        except (PyMongoError, BSONError) as error:
            raise self._query_db_error(error) from error

    async def find_one_and_update(self, collection: str, query: dict,
                                  data: dict) -> _DocumentType:
        """Retrieve a document by search and update at database collection."""
        try:
            db = self.client[self.database]
            coll = db[collection]
            await coll.find_one_and_update(
                query, data, return_document=ReturnDocument.AFTER)
        except (PyMongoError, BSONError) as error:
            raise self._query_db_error(error) from error

    async def ping(self) -> dict:
        """Check application is connected with database."""
        db = self.client[self.database]
        return await db.command({"ping": 1})
