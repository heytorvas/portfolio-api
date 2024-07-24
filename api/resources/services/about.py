from api.domain.models.about import About
from api.resources.schemas.about import AboutSchema
from api.resources.services.base import BaseService


class AboutService(BaseService):
    model = About
    schema = AboutSchema
