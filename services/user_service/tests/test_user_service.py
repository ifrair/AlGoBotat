from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Generator
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from sqlalchemy.orm import Session as SASession

from db.model import DBUser
from service.exceptions import (
    UserBannedException,
    UserNotFoundByEmailException,
    UserNotFoundException,
)
from service.schemes import UserResponse, UserResponseProvider, UserYandex
from service.user_servcie import UserService


class TestUserService:
    @pytest.mark.positive
    def test_user_exists(self, mock_repo: MagicMock, user_service: UserService, make_dbuser: DBUser):
        user_id = uuid4()
        mock_repo.get_by_id.return_value = make_dbuser

        user_service.assert_user_exists(user_id)

        mock_repo.get_by_id.assert_called_once()

    @pytest.mark.negative
    def test_user_not_found(self, mock_repo: MagicMock, user_service: UserService):
        user_id = uuid4()
        mock_repo.get_by_id.return_value = None

        with pytest.raises(UserNotFoundException):
            user_service.assert_user_exists(user_id)

    @pytest.mark.negative
    def test_assert_not_banned_user_not_found(self, mock_repo: MagicMock, user_service: UserService):
        user_id = uuid4()
        mock_repo.get_by_id.return_value = None

        with pytest.raises(UserNotFoundException):
            user_service.assert_user_not_banned(user_id)

    @pytest.mark.negative
    def test_user_is_banned(self, mock_repo: MagicMock, user_service: UserService, make_dbuser: DBUser):
        user_id = uuid4()
        make_dbuser.is_banned = True
        mock_repo.get_by_id.return_value = make_dbuser

        with pytest.raises(UserBannedException):
            user_service.assert_user_not_banned(user_id)

    @pytest.mark.positive
    def test_user_not_banned_with_provided_user(self, mock_repo: MagicMock, make_dbuser: DBUser):
        make_dbuser.is_banned = False
        mock_session = MagicMock(spec=SASession)

        @contextmanager
        def session_provider() -> Generator[Any, Any, None]:
            yield mock_session

        mock_repo.get_user_session = MagicMock(wraps=session_provider)
        service = UserService(user_repo=mock_repo)
        service._session_provider = session_provider

        service.assert_user_not_banned(make_dbuser.id, user=make_dbuser)

        mock_repo.get_by_id.assert_not_called()

    @pytest.mark.positive
    def test_get_user_profile_success(self, mock_repo: MagicMock, user_service: UserService, make_dbuser: DBUser):
        user_id = uuid4()
        mock_repo.get_by_id.return_value = make_dbuser

        result = user_service.get_user_profile(user_id)

        assert isinstance(result, UserResponse)
        assert result.id == make_dbuser.id

    @pytest.mark.negative
    def test_get_user_profile_not_found(self, mock_repo: MagicMock, user_service: UserService):
        user_id = uuid4()
        mock_repo.get_by_id.return_value = None

        with pytest.raises(UserNotFoundException):
            user_service.get_user_profile(user_id)


    @pytest.mark.positive
    def test_save_new_user(self, mock_repo: MagicMock, user_service: UserService, make_dbuser: DBUser):
        yandex_sso = UserYandex(
            id=12345,
            login="yandex_user",
            default_email="user@yandex.ru",
            emails=["user@yandex.ru"],
        )
        new_user_id = uuid4()
        make_dbuser.id = new_user_id
        mock_repo.get_user_by_yandex_sso.return_value = None
        mock_repo.save_user_profile_from_yandex.return_value = new_user_id
        mock_repo.get_by_id.return_value = make_dbuser

        with patch.object(UserResponseProvider, "from_user_db") as mock_from:
            mock_from.return_value = UserResponse.model_validate(make_dbuser)
            result = user_service.save_user_or_get_profile_from_yandex(yandex_sso=yandex_sso)

        assert result.id == new_user_id
        mock_repo.save_user_profile_from_yandex.assert_called_once()

    @pytest.mark.negative
    def test_save_user_not_found_after_insert(
        self, mock_repo: MagicMock, user_service: UserService
    ):
        yandex_sso = UserYandex(
            id=12345,
            login="yandex_user",
            default_email="user@yandex.ru",
            emails=["user@yandex.ru"],
        )
        mock_repo.get_user_by_yandex_sso.return_value = None
        mock_repo.save_user_profile_from_yandex.return_value = uuid4()
        mock_repo.get_by_id.return_value = None

        with pytest.raises(UserNotFoundException):
            user_service.save_user_or_get_profile_from_yandex(yandex_sso=yandex_sso)

    @pytest.mark.positive
    def test_update_existing_user(self, mock_repo: MagicMock, user_service: UserService, make_dbuser: DBUser):
        yandex_sso = UserYandex(
            id=12345,
            login="yandex_user",
            default_email="user@yandex.ru",
            emails=["user@yandex.ru"],
        )
        mock_repo.get_user_by_yandex_sso.return_value = make_dbuser
        mock_repo.get_by_id.return_value = make_dbuser

        with patch.object(UserResponseProvider, "from_user_db") as mock_from:
            mock_from.return_value = UserResponse.model_validate(make_dbuser)
            result = user_service.save_user_or_get_profile_from_yandex(yandex_sso=yandex_sso)

        assert result.id == make_dbuser.id
        mock_repo.update_user_profile_from_yandex.assert_called_once()


    @pytest.mark.positive
    def test_list_users(self, mock_repo: MagicMock, user_service: UserService, make_dbuser: DBUser):
        u1 = make_dbuser
        mock_repo.list_all.return_value = [u1, make_dbuser]

        result = user_service.list_users()

        assert len(result) == 2
        assert all(isinstance(u, UserResponse) for u in result)

    @pytest.mark.positive
    def test_list_users_empty(self, mock_repo: MagicMock, user_service: UserService):
        mock_repo.list_all.return_value = []

        result = user_service.list_users()

        assert result == []


    @pytest.mark.positive
    def test_get_by_email_success(self, mock_repo: MagicMock, user_service: UserService, make_dbuser: DBUser):
        email = "test@example.com"
        make_dbuser.email = email
        mock_repo.get_by_email.return_value = make_dbuser

        result = user_service.get_user_profile_by_email(email)

        assert isinstance(result, UserResponse)
        assert result.email == email

    @pytest.mark.negative
    def test_get_by_email_not_found(self, mock_repo: MagicMock, user_service: UserService):
        email = "missing@example.com"
        mock_repo.get_by_email.return_value = None

        with pytest.raises(UserNotFoundByEmailException):
            user_service.get_user_profile_by_email(email)
