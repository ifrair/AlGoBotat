import os

import pytest

from service.schemes import UserYandex
from db.user_repo import UserRepo
from service.user_service import UserService
from service.yandex_sso_service import YandexSSOService


@pytest.fixture(scope="session")
def user_service(user_repo: UserRepo) -> UserService:
    return UserService(user_repo=user_repo)

@pytest.fixture(scope="session")
def user_repo() -> UserRepo:
    return UserRepo()

@pytest.fixture(scope="session")
def token_url()->str:
    return os.getenv("YANDEX_TOKEN_URL", "https://oauth.yandex.com/token")
@pytest.fixture(scope="session")
def yandex_login_url()->str:
    return os.getenv("YANDEX_LOGIN_URL","https://login.yandex.ru/info")

@pytest.fixture(scope="session")
def user_yandex()->UserYandex:
    return UserYandex(
        id=1002,
        login="crazyocto",
        default_email="crazyocto@example.com",
        emails=["crazyocto@work.com", "crazyocto@personal.com"],
        real_name="Jane Doe",
        first_name="Jane",
        last_name="Doe",
        display_name="JD",
        birthday="1988-07-15",
        default_phone={"country_code": "1", "number": "5551234567"},
        default_avatar_id="avatar_abc123"
    )




@pytest.fixture(scope="session")
def yandex_sso_service():
    return YandexSSOService()