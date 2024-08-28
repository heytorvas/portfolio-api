from uuid import uuid4

import pytest
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND

from tests.utils import about_default_payload


class TestAboutV1:
    ENDPOINT = '/v1/about'

    def test_create_about_with_success(self, user, client):
        payload = about_default_payload(user)
        response = client.post(self.ENDPOINT, json=payload)
        response_json = response.json()

        payload['id'] = response_json.get('id')

        assert response.status_code == HTTP_201_CREATED
        assert response_json == payload

    def test_get_about_by_id_with_success(self, user, client):
        payload = about_default_payload(user)
        response = client.post(self.ENDPOINT, json=payload)
        response_json = response.json()

        payload["id"] = response_json.get("id")

        response = client.get(f"{self.ENDPOINT}/{payload['id']}")

        assert response.status_code == HTTP_200_OK
        assert response_json == payload

    def test_create_about_using_user_not_found_with_error(self, client):
        payload = about_default_payload(str(uuid4()))
        response = client.post(self.ENDPOINT, json=payload)
        response_json = response.json()

        assert response.status_code == HTTP_404_NOT_FOUND
        assert response_json["error"]["code"] == 40410
        assert response_json["error"][
                   "message"] == "User not found in database."

    @pytest.mark.parametrize('language,expected_value', [
        ('en', {'summary': 'Summary English'}),
        ('pt', {'summary': 'Summary Portuguese'})
    ])
    def test_get_about_by_language_with_success(self, client, about, language,
                                                expected_value):
        response = client.get(f"{self.ENDPOINT}/{about}?language={language}")
        response_json = response.json()

        assert response.status_code == HTTP_200_OK
        assert response_json['id'] == about
        assert response_json['summary'] == expected_value['summary']
