from api.app import build_app
from api.bootstrap import BootstrapContainer
from api.config import settings

settings = settings.from_env('default')
bootstrap = BootstrapContainer.from_setings(settings)

app = build_app(bootstrap.mongo_database)
