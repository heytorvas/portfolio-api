from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND
from uuid import uuid4
from tests.utils import user_default_payload


class TestUsersV1:
    ENDPOINT = "/v1/users"

    def test_create_user_with_success(self, client):
        payload = user_default_payload()
        response = client.post(self.ENDPOINT, json=payload)
        response_json = response.json()

        assert response.status_code == HTTP_201_CREATED
        assert response_json["id"]
        assert response_json["name"] == payload["name"]
        assert response_json["email"] == payload["email"]
        assert response_json["phone"] == payload["phone"]
        assert not response_json.get("password", None)

    def test_get_user_by_id_with_success(self, client):
        payload = user_default_payload()
        response = client.post(self.ENDPOINT, json=payload)
        response_json = response.json()
        user_id = response_json["id"]

        payload["id"] = user_id
        payload.pop("password", None)

        response = client.get(f"{self.ENDPOINT}/{user_id}")
        response_json = response.json()

        assert response.status_code == HTTP_200_OK
        assert response_json == payload

    def test_get_user_by_id_not_found_with_error(self, client):
        response = client.get(f"{self.ENDPOINT}/{uuid4()}")
        response_json = response.json()

        assert response.status_code == HTTP_404_NOT_FOUND
        assert response_json["error"]["code"] == 40410
        assert response_json["error"]["message"] == "User not found in database."
