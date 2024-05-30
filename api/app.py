from fastapi import FastAPI

from api.config import settings
from api.data.mongo import MongoDatabase
from api.errors import error_handler
from api.resources.routes import health


def build_app(mongo_database: MongoDatabase) -> FastAPI:
    """Create and configure a FastAPI application."""
    app = FastAPI(title=settings.PROJECT_NAME)

    app.include_router(health.build_router(mongo_database),
                       prefix='/health',
                       tags=['health'])

    error_handler(app)

    @app.get('/')
    async def _():
        return {'msg': 'hello world'}

    return app
