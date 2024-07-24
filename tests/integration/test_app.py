import pytest
from uuid import uuid4

from api.config import settings
from api.main import app


class TestApp:
    def test_registered_routes(self):
        all_routes = [route.path for route in app.routes]
        expected = {
            "/docs",
            "/redoc",
            "/openapi.json",
            "/health",
        }
        assert expected.issubset(all_routes)

    def test_auto_api_documentation(self, client):
        assert client.get("/docs").status_code == 200
        assert client.get("/redoc").status_code == 200
        response = client.get("/openapi.json")
        openapi = response.json()
        assert response.status_code == 200
        assert openapi["info"]["title"] == settings.PROJECT_NAME

    def test_endpoint_hello_world(self, client):
        response = client.get("")
        assert response.status_code == 200
        assert response.json() == {"msg": "hello world"}

    @pytest.mark.parametrize("endpoint", ["/v1/educations", "/v1/experiences"])
    def test_get_endpoints_by_invalid_language_with_error(self, client, endpoint):
        response = client.get(f"{endpoint}/{uuid4()!s}?language=abc")
        response_json = response.json()

        assert response.status_code == 422
        assert response_json["error"]["code"] == 42200
        assert response_json["error"]["message"] == "Validation error."
        assert response_json["error"]["errors"]
