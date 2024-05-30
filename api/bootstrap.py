from typing import NamedTuple, Self

import dynaconf
from motor.motor_asyncio import AsyncIOMotorClient

from api.data.mongo import MongoDatabase


class BootstrapContainer(NamedTuple):
    """Bootstrap container for application."""

    mongo_client: AsyncIOMotorClient
    mongo_database: MongoDatabase

    @classmethod
    def from_setings(cls, settings: dynaconf.LazySettings) -> Self:
        """Load application components by settings."""
        mongo_client = AsyncIOMotorClient(host=settings.MONGO_HOSTNAME,
                                          port=settings.MONGO_PORT,
                                          username=settings.MONGO_USERNAME,
                                          password=settings.MONGO_PASSWORD,
                                          ssl=settings.MONGO_SSL)

        mongo_database = MongoDatabase(mongo_client, settings.MONGO_DATABASE)

        return cls(mongo_client=mongo_client, mongo_database=mongo_database)

    @classmethod
    def from_env(cls, environment: str) -> Self:
        """Set environment for load settings."""
        from config import settings
        settings = settings.from_env(environment)
        return cls.from_setings(settings)
