import dataclasses
from uuid import UUID

from loguru import logger

from db.model import DBUser
from db.user_repo import UserRepo
from service.jwt_service import JwtService
from service.model import User, JWTUser
from service.schemes import LoginData
from service.yandex_sso_service import YandexSSOService


@dataclasses.dataclass
class UserService:
    user_repo: UserRepo = UserRepo()
    yandex_sso_service= YandexSSOService()
    jwt_service=JwtService()

    def get_user_by_email(self, email: str):
        return self._to_dao_user(user=self.user_repo.get_user_by_email(email=email))

    def get_user_by_yandex_id(self, email: str):
        return self._to_dao_user(user=self.user_repo.get_user_by_yandex_id(email=email))

    def get_user_by_id(self, user_id: UUID):
        return self._to_dao_user(user=self.user_repo.get_user_by_id(user_id=user_id))

    def login(self, sso_data: LoginData) -> str:
        logger.debug("Авторизация по данным пользователя %r...", sso_data.data)

        user = self.save_user_or_get_profile_from_yandex(code=sso_data.data)

        jwt_token = self.jwt_service.generate_jwt_token(user=JWTUser(user_id=str(user.id), role=user.role))

        logger.debug("Пользователь %r успешно авторизовался.", user)

        return jwt_token

    @staticmethod
    def _to_dao_user(user: DBUser)-> User:
        return User(id=user.id, username=user.username, first_name=user.first_name, last_name=user.last_name, bio=user.bio, email=user.email, is_test_user=user.is_test_user, is_banned=user.is_banned, created_at=user.created_at, updated_at=user.updated_at)


    def save_user_or_get_profile_from_yandex(
            self, code: str, is_test_user: bool = False
    ) -> DBUser:
        yandex_sso = self.yandex_sso_service.fetch_user_data(code=code)
        user = self.user_repo.get_user_by_yandex_sso(yandex_id=yandex_sso.id)

        if user is None:
            self.user_repo.save_user_profile_from_yandex(
                yandex_sso=yandex_sso, is_test_user=is_test_user
            )
            user = self.user_repo.get_user_by_yandex_sso(yandex_id=yandex_sso.id)

        else:
            self.user_repo.update_user_profile_from_yandex(
                yandex_sso=yandex_sso, user_id=user.id
            )
            user = self.user_repo.get_user_by_yandex_sso(yandex_id=yandex_sso.id)

        return user
