from uuid import uuid4

import pytest
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND
from tests.utils import education_default_payload


class TestEducationsV1:
    ENDPOINT = "/v1/educations"

    def test_create_education_with_success(self, user, client):
        payload = education_default_payload(user)
        response = client.post(self.ENDPOINT, json=payload)
        response_json = response.json()

        payload["id"] = response_json.get("id")

        assert response.status_code == HTTP_201_CREATED
        assert response_json == payload

    def test_get_education_by_id_with_success(self, user, client):
        payload = education_default_payload(user)
        response = client.post(self.ENDPOINT, json=payload)
        response_json = response.json()

        payload["id"] = response_json.get("id")

        response = client.get(f'{self.ENDPOINT}/{payload['id']}')

        assert response.status_code == HTTP_200_OK
        assert response_json == payload

    def test_create_education_using_user_not_found_with_error(self, client):
        payload = education_default_payload(str(uuid4()))
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
                    "degree": "Degree English",
                    "school": "School English",
                    "course": "Course English",
                },
            ),
            (
                "pt",
                {
                    "degree": "Degree Portuguese",
                    "school": "School Portuguese",
                    "course": "Course Portuguese",
                },
            ),
        ],
    )
    def test_get_education_by_language_with_success(
        self, client, education, language, expected_value
    ):
        response = client.get(f"{self.ENDPOINT}/{education}?language={language}")
        response_json = response.json()

        assert response.status_code == HTTP_200_OK
        assert response_json["id"] == education
        assert response_json["degree"] == expected_value["degree"]
        assert response_json["school"] == expected_value["school"]
        assert response_json["course"] == expected_value["course"]
