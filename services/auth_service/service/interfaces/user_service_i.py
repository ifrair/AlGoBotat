import dataclasses
import os
from uuid import UUID

from abc import ABC, abstractmethod
from loguru import logger

from services.user_service.db.model import DBUser
from services.user_service.db.user_repo import UserRepo
from service.jwt_service import JwtService
from service.model import User, JWTUser
from service.schemes import LoginData, UserYandex
from service.yandex_sso_service import YandexSSOService


@dataclasses.dataclass
class UserServiceI(ABC):
    @abstractmethod
    def get_user_by_yandex_sso(self, yandex_id: int) -> User:
        pass

    @abstractmethod
    def save_user_profile_from_yandex(
        self, yandex_sso: UserYandex, is_test_user: bool
    ) -> User:
        pass

    @abstractmethod
    def update_user_profile_from_yandex(
        self, yandex_sso: UserYandex, user_id: UUID
    ) -> None:
        pass
