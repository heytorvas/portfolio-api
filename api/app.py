from fastapi import FastAPI

from api.config import settings
from api.data.mongo import MongoDatabase
from api.errors import error_handler
from api.resources.routes import experience, health
from api.resources.services.experience import ExperienceService


def build_app(mongo_database: MongoDatabase,
              experience_service: ExperienceService) -> FastAPI:
    """Create and configure a FastAPI application."""
    app = FastAPI(title=settings.PROJECT_NAME)

    app.include_router(health.build_router(mongo_database),
                       prefix='/health',
                       tags=['health'])
    app.include_router(experience.build_router(experience_service),
                       prefix='/v1/experiences',
                       tags=['experiences'])

    error_handler(app)

    @app.get('/')
    async def _():
        return {'msg': 'hello world'}

    return app
