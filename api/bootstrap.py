from typing import NamedTuple

import dynaconf
from mongomock_motor import AsyncMongoMockClient
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from typing_extensions import Self

from api.data.mongo import MongoDatabase
from api.domain.repositories.about import AboutRepository
from api.domain.repositories.education import EducationRepository
from api.domain.repositories.experience import ExperienceRepository
from api.domain.repositories.user import UserRepository
from api.resources.services.about import AboutService
from api.resources.services.education import EducationService
from api.resources.services.experience import ExperienceService
from api.resources.services.user import UserService


class BootstrapContainer(NamedTuple):
    """Bootstrap container for application."""

    mongo_client: AsyncIOMotorClient
    mongo_database: MongoDatabase
    experience_repository: ExperienceRepository
    experience_service: ExperienceService
    user_repository: UserRepository
    user_service: UserService
    education_repository: EducationRepository
    education_service: EducationService
    about_repository: AboutRepository
    about_service: AboutService

    @classmethod
    def from_settings(cls, settings: dynaconf.LazySettings) -> Self:
        """Load application components by settings."""
        if settings.ENVIRONMENT == "prd":
            mongo_uri = f"mongodb+srv://{settings.MONGO_USERNAME}:{settings.MONGO_PASSWORD}@{settings.MONGO_HOSTNAME}"
            mongo_client = AsyncIOMotorClient(mongo_uri,
                                              server_api=ServerApi("1"))
        elif settings.ENVIRONMENT == "test":
            mongo_client = AsyncMongoMockClient()
        else:
            mongo_client = AsyncIOMotorClient(
                host=settings.MONGO_HOSTNAME,
                port=settings.MONGO_PORT,
                username=settings.MONGO_USERNAME,
                password=settings.MONGO_PASSWORD,
                ssl=settings.MONGO_SSL,
                uuidRepresentation=settings.MONGO_OPTIONS_UUIDREPRESENTATION,
            )

        mongo_database = MongoDatabase(mongo_client, settings.MONGO_DATABASE)
        experience_repository = ExperienceRepository(
            mongo_database, settings.MONGO_EXPERIENCE_COLLECTION)
        experience_service = ExperienceService(experience_repository)
        user_repository = UserRepository(mongo_database,
                                         settings.MONGO_USER_COLLECTION)
        user_service = UserService(user_repository)
        education_repository = EducationRepository(
            mongo_database, settings.MONGO_EDUCATION_COLLECTION)
        education_service = EducationService(education_repository)
        about_repository = AboutRepository(mongo_database,
                                           settings.MONGO_ABOUT_COLLECTION)
        about_service = AboutService(about_repository)

        return cls(mongo_client=mongo_client,
                   mongo_database=mongo_database,
                   experience_repository=experience_repository,
                   experience_service=experience_service,
                   user_repository=user_repository,
                   user_service=user_service,
                   education_repository=education_repository,
                   education_service=education_service,
                   about_repository=about_repository,
                   about_service=about_service)

    @classmethod
    def from_env(cls, environment: str) -> Self:
        """Set environment for load settings."""
        from config import settings

        settings = settings.from_env(environment)
        return cls.from_settings(settings)
