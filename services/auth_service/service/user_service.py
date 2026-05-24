import dataclasses
import os
from datetime import datetime
from typing import override
from uuid import UUID

from loguru import logger

from service.exceptions import YandexDataError
from service.interfaces.user_service_i import UserServiceI
from service.yandex_sso_service import YandexSSOService
from services.commons.constants import UserRole
from service.jwt_service import JwtService
from service.model import User, JWTUser
from service.schemes import LoginData, UserYandex


@dataclasses.dataclass
class UserServiceMock(UserServiceI):
    jwt_service = JwtService()
    user_service_url = os.getenv("USER_SERVICE_URL", "http://user_service/api/v1")

    def update_user_profile_from_yandex(self, yandex_sso: UserYandex, user_id: UUID):
        pass

    @override
    def get_user_by_yandex_sso(self, yandex_id: int):
        return self._get_mock_user(yandex_id=str(yandex_id))

    @override
    def save_user_profile_from_yandex(self, yandex_sso: UserYandex, is_test_user: bool):
        return self._get_mock_user(
            email=yandex_sso.default_email, yandex_id=str(yandex_sso.id)
        )

    def _get_user_by_yandex_id(self, yandex_id: str):
        return self._get_mock_user(yandex_id=yandex_id)

    @staticmethod
    def _get_mock_user(**kwargs) -> User:
        return User.model_validate(
            {
                "yandex_id": "123234345",
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "id": UUID("810948d3-ecc7-4cf0-af20-6649c136abe3"),
                "email": "admin@aibotat.com",
                "role": UserRole.USER,
            }
            | kwargs
        )
