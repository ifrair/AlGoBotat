import dataclasses
from uuid import UUID

from loguru import logger
from sqlalchemy import select

from services.auth_service.db.model import DBUser, DBUserYandexSSO
from services.auth_service.db.user_repo import UserRepo
from services.auth_service.service.model import User
from services.auth_service.service.schemes import UserYanex
from services.auth_service.service.yandex_sso_service import YandexSSOService


@dataclasses.dataclass
class UserService:
    user_repo: UserRepo = UserRepo()
    yandex_sso_service= YandexSSOService()

    def get_user_by_email(self, email: str):
        return self._to_dao_user(user=self.user_repo.get_user_by_email(email=email))

    def get_user_by_yandex_id(self, email: str):
        return self._to_dao_user(user=self.user_repo.get_user_by_yandex_id(email=email))

    def get_user_by_id(self, user_id: UUID):
        return self._to_dao_user(user=self.user_repo.get_user_by_id(user_id=user_id))


    @staticmethod
    def _to_dao_user(user: DBUser)-> User:
        return User(id=user.id, username=user.username, first_name=user.first_name, last_name=user.last_name, bio=user.bio, email=user.email, is_test_user=user.is_test_user, is_banned=user.is_banned, created_at=user.created_at, updated_at=user.updated_at)


    def save_user_or_get_profile_from_yandex(
            self, code: str, is_test_user: bool = False
    ) -> DBUser:
        yandex_sso = self.yandex_sso_service.fetch_user_data(code=code)
        user = self.user_repo.get_user_by_yandex_sso(yandex_id=code)

        if user is None:
            user_id = self.user_repo.save_user_profile_from_yandex(
                yandex_sso=yandex_sso, is_test_user=is_test_user
            )
            user = self.user_repo.get_user_by_id(user_id=user_id)

        else:
            self.user_repo.update_user_profile_from_yandex(
                yandex_sso=yandex_sso, user_id=user.id
            )
            user = self.user_repo.get_user_by_id(user_id=user.id)

        return user