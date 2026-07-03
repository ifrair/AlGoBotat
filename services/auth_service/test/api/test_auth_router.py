from http import HTTPStatus

import pytest
import responses
from fastapi.testclient import TestClient

from api.app import app


@pytest.fixture
def client():
    return TestClient(app)


class TestAuthRouterLogin:
    @pytest.mark.positive
    @responses.activate
    def test_login_success(self, client, user_yandex, token_url, yandex_login_url):
        responses.add(
            responses.POST,
            token_url,
            json={"access_token": "some_token"},
            status=HTTPStatus.OK,
        )
        responses.add(
            responses.GET,
            yandex_login_url,
            json=user_yandex.model_dump(),
            status=HTTPStatus.OK,
        )

        payload = {"auth_type": "YANDEX_SSO", "data": "valid_code"}
        response = client.post("/api/v1/auth/login", json=payload)

        assert response.status_code == HTTPStatus.OK
        assert isinstance(response.text, str)
        assert len(response.text) > 0

    @pytest.mark.negative
    def test_login_invalid_auth_type(self, client):
        payload = {"auth_type": "INVALID_TYPE", "data": "some_code"}
        response = client.post("/api/v1/auth/login", json=payload)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    @pytest.mark.negative
    def test_login_missing_data(self, client):
        payload = {"auth_type": "YANDEX_SSO"}
        response = client.post("/api/v1/auth/login", json=payload)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    @pytest.mark.negative
    @responses.activate
    def test_login_empty_data(self, client, token_url):
        responses.add(
            responses.POST,
            token_url,
            json={"error": "invalid_request"},
            status=HTTPStatus.BAD_REQUEST,
        )

        payload = {"auth_type": "YANDEX_SSO", "data": ""}
        response = client.post("/api/v1/auth/login", json=payload)

        assert response.status_code == HTTPStatus.BAD_REQUEST

    @pytest.mark.negative
    def test_login_empty_body(self, client):
        response = client.post("/api/v1/auth/login", json={})

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    @pytest.mark.negative
    @responses.activate
    def test_login_yandex_token_error(self, client, token_url):
        responses.add(
            responses.POST,
            token_url,
            json={"error": "invalid_grant"},
            status=HTTPStatus.BAD_REQUEST,
        )

        payload = {"auth_type": "YANDEX_SSO", "data": "bad_code"}
        response = client.post("/api/v1/auth/login", json=payload)

        assert response.status_code == HTTPStatus.BAD_REQUEST

    @pytest.mark.negative
    @responses.activate
    def test_login_yandex_data_error(
        self, client, user_yandex, token_url, yandex_login_url
    ):
        responses.add(
            responses.POST,
            token_url,
            json={"access_token": "some_token"},
            status=HTTPStatus.OK,
        )
        responses.add(
            responses.GET,
            yandex_login_url,
            json={"error": "unauthorized"},
            status=HTTPStatus.UNAUTHORIZED,
        )

        payload = {"auth_type": "YANDEX_SSO", "data": "valid_code"}
        response = client.post("/api/v1/auth/login", json=payload)

        assert response.status_code == HTTPStatus.BAD_REQUEST

    @pytest.mark.negative
    def test_login_wrong_method_get(self, client):
        response = client.get("/api/v1/auth/login")
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    @pytest.mark.negative
    def test_login_wrong_path(self, client):
        payload = {"auth_type": "YANDEX_SSO", "data": "some_code"}
        response = client.post("/api/v1/auth/wrong", json=payload)
        assert response.status_code == HTTPStatus.NOT_FOUND
