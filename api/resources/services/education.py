from api.domain.models.education import Education
from api.resources.schemas.education import EducationSchema
from api.resources.services.base import BaseService


class EducationService(BaseService):
    """Service class for education context."""

    model = Education
    schema = EducationSchema
