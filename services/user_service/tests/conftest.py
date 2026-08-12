from __future__ import annotations

# mypy: ignore-errors
import logging
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Any, Generator
from unittest.mock import MagicMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session as SASession

from db.user_repo import UserRepo
from api.app import app
from api.dependencies import require_admin
from db.model import DBUser
from service.user_servcie import UserService

logger = logging.getLogger(__name__)


@pytest.fixture
def override_admin():
    app.dependency_overrides[require_admin] = lambda: None
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def client(override_admin: None) -> TestClient:
    return TestClient(app)


@pytest.fixture
def make_dbuser() -> DBUser:
    uid = uuid4()
    now = datetime.now(timezone.utc)
    user = MagicMock(spec=DBUser, id=uid)
    user.id = uid
    user.username = "test_user"
    user.first_name = "Test"
    user.last_name = "User"
    user.bio = None
    user.email = "test@example.com"
    user.photo_url = None
    user.role = "user"
    user.is_banned = False
    user.is_test_user = False
    user.created_at = now
    user.updated_at = now
    return user


@pytest.fixture(scope="session")
def user_repo() -> UserRepo:
    return UserRepo()


@pytest.fixture(scope="function")
def session(user_repo: UserRepo) -> Generator[SASession, None, None]:
    with user_repo.get_user_session() as s:
        yield s


@pytest.fixture(scope="session", autouse=True)
def prepare_data(user_repo: UserRepo) -> None:
    with user_repo.get_user_session() as session:
        user_repo.delete_test_users(session=session)
        for _ in range(100):
            user_repo.generate_and_save_random_user(session=session)


@pytest.fixture
def get_random_user_id(user_repo: UserRepo, session: SASession) -> UUID:
    ids = user_repo.list_all(session=session)
    test_users = [u for u in ids if u.is_test_user]
    if test_users:
        return test_users[0].id
    return user_repo.generate_and_save_random_user(session=session)


@pytest.fixture
def mock_repo() -> MagicMock:
    return MagicMock()


@pytest.fixture
def user_service(mock_repo: MagicMock) -> UserService:
    mock_session = MagicMock(spec=SASession)

    @contextmanager
    def session_provider() -> Generator[Any, Any, None]:
        yield mock_session

    mock_repo.get_user_session = session_provider
    service = UserService(user_repo=mock_repo)
    service._session_provider = session_provider
    return service
