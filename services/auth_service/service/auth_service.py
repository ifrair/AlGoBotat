import dataclasses
from dataclasses import field
from typing import override
from uuid import UUID

from loguru import logger
from requests.utils import default_user_agent

from service.interfaces.auth_service_i import AuthServiceI
from service.interfaces.user_service_i import UserServiceI
from service.user_service import UserServiceMock
from service.jwt_service import JwtService
from service.model import User, JWTUser
from service.schemes import LoginData
from service.yandex_sso_service import YandexSSOService


@dataclasses.dataclass
class AuthService(AuthServiceI):
    user_service: UserServiceI = field(default_factory=UserServiceMock)
    yandex_sso_service = YandexSSOService()
    jwt_service = JwtService()

    @override
    def login(self, sso_data: LoginData) -> str:
        logger.debug("Авторизация по данным пользователя %r...", sso_data.data)

        user = self._save_user_or_get_profile_from_yandex(code=sso_data.data)

        jwt_token = self.jwt_service.generate_jwt_token(
            user=JWTUser(user_id=str(user.id), role=user.role)
        )

        logger.debug("Пользователь %r успешно авторизовался.", user)

        return jwt_token

    def _save_user_or_get_profile_from_yandex(
        self, code: str, is_test_user: bool = False
    ) -> User:
        yandex_sso = self.yandex_sso_service.fetch_user_data(code=code)
        user = self.user_service.get_user_by_yandex_sso(yandex_id=yandex_sso.id)

        if user is None:
            self.user_service.save_user_profile_from_yandex(
                yandex_sso=yandex_sso, is_test_user=is_test_user
            )
            user = self.user_service.get_user_by_yandex_sso(yandex_id=yandex_sso.id)

        else:
            self.user_service.update_user_profile_from_yandex(
                yandex_sso=yandex_sso, user_id=user.id
            )
            user = self.user_service.get_user_by_yandex_sso(yandex_id=yandex_sso.id)

        return User
