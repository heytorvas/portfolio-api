from api.domain.models.user import User
from api.resources.schemas.user import UserSchema
from api.resources.services.base import BaseService


class UserService(BaseService):
    """Service class for user context."""

    schema = UserSchema
    model = User
