from typing import NamedTuple

import dynaconf
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from typing_extensions import Self

from api.data.mongo import MongoDatabase
from api.domain.repositories.experience import ExperienceRepository
from api.resources.services.experience import ExperienceService


class BootstrapContainer(NamedTuple):
    """Bootstrap container for application."""

    mongo_client: AsyncIOMotorClient
    mongo_database: MongoDatabase
    experience_repository: ExperienceRepository
    experience_service: ExperienceService

    @classmethod
    def from_setings(cls, settings: dynaconf.LazySettings) -> Self:
        """Load application components by settings."""
        if settings.ENVIRONMENT == 'prd':
            mongo_uri = f'mongodb+srv://{settings.MONGO_USERNAME}:{settings.MONGO_PASSWORD}@{settings.MONGO_HOSTNAME}'
            mongo_client = AsyncIOMotorClient(mongo_uri,
                                              server_api=ServerApi('1'))
        else:
            mongo_client = AsyncIOMotorClient(
                host=settings.MONGO_HOSTNAME,
                port=settings.MONGO_PORT,
                username=settings.MONGO_USERNAME,
                password=settings.MONGO_PASSWORD,
                ssl=settings.MONGO_SSL,
                uuidRepresentation=settings.MONGO_OPTIONS_UUIDREPRESENTATION)

        mongo_database = MongoDatabase(mongo_client, settings.MONGO_DATABASE)
        experience_repository = ExperienceRepository(
            mongo_database, settings.MONGO_EXPERIENCE_COLLECTION)
        experience_service = ExperienceService(experience_repository)

        return cls(mongo_client=mongo_client,
                   mongo_database=mongo_database,
                   experience_repository=experience_repository,
                   experience_service=experience_service)

    @classmethod
    def from_env(cls, environment: str) -> Self:
        """Set environment for load settings."""
        from config import settings
        settings = settings.from_env(environment)
        return cls.from_setings(settings)
