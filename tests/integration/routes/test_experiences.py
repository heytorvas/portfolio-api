from uuid import uuid4

import pytest

from tests.utils import experience_default_payload
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND


class TestExperiencesV1:
    ENDPOINT = "/v1/experiences"

    def test_create_experience_with_success(self, user, client):
        payload = experience_default_payload(user)
        response = client.post(self.ENDPOINT, json=payload)
        response_json = response.json()

        payload["id"] = response_json["id"]

        assert response.status_code == HTTP_201_CREATED
        assert response_json

    def test_get_experience_by_id_with_success(self, client, experience, user):
        payload = experience_default_payload(user)
        response = client.get(f"{self.ENDPOINT}/{experience}")
        response_json = response.json()

        payload["id"] = response_json.get("id")

        assert response.status_code == HTTP_200_OK
        assert response_json == payload

    def test_create_experience_using_user_not_found_with_error(self, client):
        payload = experience_default_payload(str(uuid4()))
        response = client.post(self.ENDPOINT, json=payload)
        response_json = response.json()

        assert response.status_code == HTTP_404_NOT_FOUND
        assert response_json["error"]["code"] == 40410
        assert response_json["error"]["message"] == "User not found in database."

    @pytest.mark.parametrize(
        "language,expected_value",
        [
            (
                "en",
                {
                    "role": "Role English",
                    "project": "Project English",
                    "description": "Description English",
                },
            ),
            (
                "pt",
                {
                    "role": "Role Portuguese",
                    "project": "Project Portuguese",
                    "description": "Description Portuguese",
                },
            ),
        ],
    )
    def test_get_experience_by_language_with_success(
        self, client, experience, language, expected_value
    ):
        response = client.get(f"{self.ENDPOINT}/{experience}?language={language}")
        response_json = response.json()

        assert response.status_code == HTTP_200_OK
        assert response_json["id"] == experience
        assert response_json["details"][0]["role"] == expected_value["role"]
        assert response_json["details"][0]["project"] == expected_value["project"]
        assert (
            response_json["details"][0]["description"][0]
            == expected_value["description"]
        )
