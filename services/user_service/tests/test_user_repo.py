from __future__ import annotations

from uuid import UUID, uuid4

import pytest
from sqlalchemy.orm import Session

from db.model import DBUser
from db.user_repo import UserRepo
from service.schemes import UserYandex


class TestUserRepo:
    @pytest.mark.positive
    def test_get_by_id_found(self, user_repo: UserRepo, session: Session, get_random_user_id: UUID):
        user = user_repo.get_by_id(user_id=get_random_user_id, session=session)

        assert user is not None
        assert user.id == get_random_user_id

    @pytest.mark.negative
    def test_get_by_id_not_found(self, user_repo: UserRepo, session: Session):
        user = user_repo.get_by_id(user_id=uuid4(), session=session)

        assert user is None


    @pytest.mark.positive
    def test_get_by_email_found(self, user_repo: UserRepo, session: Session):
        email = f"{uuid4().hex[:8]}@unique.test"
        user = DBUser(
            first_name="Email",
            last_name="Test",
            username="email_test",
            email=email,
            is_test_user=True,
        )
        session.add(user)
        session.flush()
        user_id = user.id
        session.commit()

        found = user_repo.get_by_email(email=email, session=session)

        assert found is not None
        assert found.id == user_id

    @pytest.mark.negative
    def test_get_by_email_not_found(self, user_repo: UserRepo, session: Session):
        found = user_repo.get_by_email(email="nonexistent@test.com", session=session)

        assert found is None


    @pytest.mark.positive
    def test_list_all_returns_users(self, user_repo: UserRepo, session: Session):
        users = user_repo.list_all(session=session)

        assert len(users) > 0
        assert all(isinstance(u, DBUser) for u in users)


    @pytest.mark.positive
    def test_delete_user_found(self, user_repo: UserRepo, session: Session, get_random_user_id: UUID):
        result = user_repo.delete(user_id=get_random_user_id, session=session)
        session.commit()

        assert result is True
        assert user_repo.get_by_id(user_id=get_random_user_id, session=session) is None


    @pytest.mark.positive
    def test_set_banned_true(self, user_repo: UserRepo, session: Session, get_random_user_id: UUID):
        user = user_repo.set_banned(user_id=get_random_user_id, banned=True, session=session)
        session.flush()

        assert user is not None
        assert user.is_banned is True

    @pytest.mark.positive
    def test_set_banned_then_false(self, user_repo: UserRepo, session: Session, get_random_user_id: UUID):
        user_repo.set_banned(user_id=get_random_user_id, banned=True, session=session)
        session.flush()

        user = user_repo.set_banned(user_id=get_random_user_id, banned=False, session=session)
        session.flush()

        assert user is not None
        assert user.is_banned is False

    @pytest.mark.positive
    def test_get_user_by_yandex_sso_found(self, user_repo: UserRepo, session: Session):
        yandex_id = uuid4().int & 0x7FFFFFFF
        yandex_sso = UserYandex(
            id=yandex_id,
            login="sso_user",
            default_email="sso@yandex.ru",
            emails=["sso@yandex.ru"],
            first_name="SSO",
            last_name="User",
            display_name="SSO User",
        )
        user_id = user_repo.save_user_profile_from_yandex(yandex_sso=yandex_sso, session=session)
        session.commit()

        result = user_repo.get_user_by_yandex_sso(yandex_id=yandex_id, session=session)

        assert result is not None
        assert result.id == user_id

    @pytest.mark.negative
    def test_get_user_by_yandex_sso_not_found(self, user_repo: UserRepo, session: Session):
        result = user_repo.get_user_by_yandex_sso(yandex_id=0, session=session)

        assert result is None


    @pytest.mark.positive
    def test_save_user_profile_from_yandex(self, user_repo: UserRepo, session: Session):
        yandex_sso = UserYandex(
            id=12345,
            login="yandex_user",
            default_email="user@yandex.ru",
            emails=["user@yandex.ru"],
            first_name="Test",
            last_name="User",
            display_name="Test User",
            default_avatar_id="avatar123",
        )

        user_id = user_repo.save_user_profile_from_yandex(
            yandex_sso=yandex_sso, session=session, is_test_user=True
        )
        session.commit()

        assert isinstance(user_id, UUID)
        user = user_repo.get_by_id(user_id=user_id, session=session)
        assert user is not None
        assert user.first_name == "Test"

    @pytest.mark.positive
    def test_save_user_profile_from_yandex_no_optional_fields(self, user_repo: UserRepo, session: Session):
        yandex_sso = UserYandex(
            id=uuid4().int & 0x7FFFFFFF,
            login="minimal_user",
            default_email="minimal@yandex.ru",
            emails=["minimal@yandex.ru"],
        )

        user_id = user_repo.save_user_profile_from_yandex(yandex_sso=yandex_sso, session=session)
        session.commit()

        assert isinstance(user_id, UUID)

    @pytest.mark.positive
    def test_update_user_profile_from_yandex(self, user_repo: UserRepo, session: Session, get_random_user_id: UUID):
        yandex_sso = UserYandex(
            id=88888,
            login="updated_user",
            default_email="updated@yandex.ru",
            emails=["updated@yandex.ru"],
            first_name="Updated",
            last_name="Name",
            display_name="Updated Name",
            default_avatar_id="avatar888",
        )

        user_repo.update_user_profile_from_yandex(
            yandex_sso=yandex_sso, user_id=get_random_user_id, session=session
        )
        session.commit()

        user = user_repo.get_by_id(user_id=get_random_user_id, session=session)
        assert user is not None
        assert user.email=="updated@yandex.ru"