from __future__ import annotations

from http import HTTPStatus
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from db.model import DBUser
from db.user_repo import UserRepo
from service.schemes import UserYandex


class TestUserApi:
    @pytest.mark.positive
    def test_admin_get_user_found(self, client: TestClient, get_random_user_id):
        user_id = get_random_user_id

        response = client.get(f"/api/v1/admin/user/{user_id}")

        assert response.status_code == HTTPStatus.OK

        data = response.json()

        assert data["id"] == str(user_id)

    @pytest.mark.negative
    def test_admin_get_user_not_found(self, client: TestClient):
        response = client.get(f"/api/v1/admin/user/{uuid4()}")

        assert response.status_code == HTTPStatus.NOT_FOUND


    @pytest.mark.positive
    def test_create_new_user(self, client: TestClient):
        yandex_id = uuid4().int & 0x7FFFFFFF
        payload = UserYandex(
            id=yandex_id,
            login="api_test_user",
            default_email="api_test@yandex.ru",
            emails=["api_test@yandex.ru"],
            first_name="API",
            last_name="Test",
            display_name="API Test",
        ).model_dump(mode="json")

        response = client.post("/api/v1/user", json=payload)

        assert response.status_code == HTTPStatus.OK

    @pytest.mark.negative
    def test_create_user_missing_fields(self, client: TestClient):
        response = client.post("/api/v1/user", json={})

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


    @pytest.mark.positive
    def test_find_by_email_found(self, client: TestClient, user_repo, session):
        email = f"{uuid4().hex[:8]}@unique.test"
        user = DBUser(
            first_name="FindByEmail",
            last_name="Test",
            username="find_email_test",
            email=email,
            is_test_user=True,
        )
        session.add(user)
        session.flush()
        user_id = user.id
        session.commit()

        response = client.get(f"/api/v1/admin/find_by_email/{email}")

        assert response.status_code == HTTPStatus.OK
        assert response.json()["id"] == str(user_id)

    @pytest.mark.negative
    def test_find_by_email_not_found(self, client: TestClient):
        response = client.get("/api/v1/admin/find_by_email/nonexistent@test.com")

        assert response.status_code == HTTPStatus.NOT_FOUND
