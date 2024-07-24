import pytest
from fastapi.testclient import TestClient

from api.app import build_app
from api.config import settings
from api.bootstrap import BootstrapContainer
from bson.binary import UuidRepresentation
from uuid import UUID
import bson
from tests.utils import (
    education_default_payload,
    user_default_payload,
    experience_default_payload, about_default_payload,
)


settings = settings.from_env("testing")

original_from_uuid = bson.binary.Binary.from_uuid


def mocked_from_uuid(
    uuid: UUID, uuid_representation: int = UuidRepresentation.STANDARD
):
    return original_from_uuid(
        uuid=uuid, uuid_representation=UuidRepresentation.STANDARD
    )


bson.binary.Binary.from_uuid = mocked_from_uuid
bootstrap = BootstrapContainer.from_settings(settings)


@pytest.fixture()
def client() -> TestClient:
    app = build_app(
        mongo_database=bootstrap.mongo_database,
        experience_service=bootstrap.experience_service,
        user_service=bootstrap.user_service,
        education_service=bootstrap.education_service,
        about_service=bootstrap.about_service
    )
    return TestClient(app)


@pytest.fixture()
def user(client) -> str:
    response = client.post("/v1/users", json=user_default_payload())
    return response.json()["id"]


@pytest.fixture()
def education(client, user) -> str:
    response = client.post("/v1/educations", json=education_default_payload(user))
    return response.json()["id"]


@pytest.fixture()
def experience(client, user) -> str:
    response = client.post("/v1/experiences", json=experience_default_payload(user))
    return response.json()["id"]

@pytest.fixture()
def about(client, user) -> str:
    response = client.post("/v1/about", json=about_default_payload(user))
    return response.json()["id"]
