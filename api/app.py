from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config import settings
from api.data.mongo import MongoDatabase
from api.errors import error_handler
from api.resources.routes import about, education, experience, health, token, \
    user
from api.resources.services.about import AboutService
from api.resources.services.education import EducationService
from api.resources.services.experience import ExperienceService
from api.resources.services.user import UserService


def build_app(mongo_database: MongoDatabase,
              experience_service: ExperienceService, user_service: UserService,
              education_service: EducationService,
              about_service: AboutService) -> FastAPI:
    """Create and configure a FastAPI application."""
    app = FastAPI(title=settings.PROJECT_NAME, debug=True)
    # app.add_middleware(RouterLoggingMiddleware,
    #                    logger=logging.getLogger(__name__))

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.build_router(mongo_database),
                       prefix="/health",
                       tags=["health"])
    app.include_router(
        experience.build_router(experience_service, user_service),
        prefix="/v1/experiences",
        tags=["experiences"],
    )
    app.include_router(
        user.build_router(user_service, experience_service, education_service,
                          about_service),
        prefix="/v1/users",
        tags=["users"],
    )
    app.include_router(
        education.builder_router(education_service, user_service),
        prefix="/v1/educations",
        tags=["educations"],
    )
    app.include_router(about.build_router(about_service, user_service),
                       prefix="/v1/about",
                       tags=["about"])
    app.include_router(token.build_router(), prefix="/token", tags=["token"])

    error_handler(app)

    @app.get("/")
    async def _():
        return {"msg": "hello world"}

    return app
