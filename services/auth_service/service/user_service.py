import dataclasses
import os
from datetime import datetime
from typing import override
from uuid import UUID

from service.interfaces.user_service_i import UserServiceI
from service.jwt_service import JwtService
from service.model import User
from service.schemes import UserYandex
from commons.constants import UserRole


@dataclasses.dataclass
class UserServiceMock(UserServiceI):
    jwt_service = JwtService()
    user_service_url = os.getenv("USER_SERVICE_URL", "http://user_service/api/v1")

    @override
    def get_or_save_user_by_yandex_sso(
        self, yandex_sso: UserYandex, is_test_user: bool = False
    ):
        return self._get_mock_user(
            email=yandex_sso.default_email, yandex_id=str(yandex_sso.id)
        )

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
