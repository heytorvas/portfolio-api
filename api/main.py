from api.app import build_app
from api.bootstrap import BootstrapContainer
from api.config import settings

settings = settings.from_env("default")
bootstrap = BootstrapContainer.from_settings(settings)

app = build_app(mongo_database=bootstrap.mongo_database,
                experience_service=bootstrap.experience_service,
                user_service=bootstrap.user_service,
                education_service=bootstrap.education_service,
                about_service=bootstrap.about_service)
