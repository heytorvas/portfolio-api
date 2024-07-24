from datetime import datetime, timedelta, timezone

import jwt
from fastapi import APIRouter
from jwt.exceptions import InvalidTokenError

from api.config import settings
from api.exceptions import UnauthorizedHTTPError


def __create_access_token(data: dict) -> dict:
    data.update({
        "exp":
        datetime.now(timezone.utc) +
        timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)
    })
    return jwt.encode(data,
                      settings.JWT_SECRET_KEY,
                      algorithm=settings.JWT_ALGORITHM)


def get_token(token: str) -> dict:
    """Validate received token from endpoints."""
    try:
        return jwt.decode(token,
                          settings.JWT_SECRET_KEY,
                          algorithms=[settings.JWT_ALGORITHM])
    except InvalidTokenError as error:
        raise UnauthorizedHTTPError("Invalid credentials") from error


def build_router() -> APIRouter:  # noqa: D103
    router = APIRouter()

    @router.post("")
    async def login(password: str):
        if password == settings.JWT_PASSWORD:
            return {
                "access_token": __create_access_token({"sub":
                                                       "administrator"}),
                "token_type": "bearer",
            }
        raise UnauthorizedHTTPError("Invalid credentials")

    return router
