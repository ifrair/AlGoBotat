import dataclasses
from typing import Any
from uuid import UUID

from db.model import DBUser
from db.user_repo import UserRepo
from service.exceptions import UserNotFoundException, UserBannedException, UserNotFoundByEmailException
from service.schemes import UserResponse
from service.schemes import UserResponseProvider, UserYandex
from service.session import SessionMixin


@dataclasses.dataclass
class UserService(SessionMixin):
    user_repo: UserRepo = UserRepo()

    def __post_init__(self):
        self._session_provider = self.user_repo.get_user_session


    def assert_user_exists(self, user_id: UUID):
        with self.get_session() as ctx:
            if (
                    self.user_repo.get_by_id(user_id=user_id, session=ctx)
                    is None
            ):
                raise UserNotFoundException(user_id)

    def assert_user_not_banned(self, user_id: UUID, user: DBUser | None = None):
        if user is None:
            with self.get_session() as ctx:
                user = self.user_repo.get_by_id(
                    user_id=user_id, session=ctx
                )
        if user is None:
            raise UserNotFoundException(user_id)
        if user.is_banned:
            raise UserBannedException(user_id)

    def delete_user(self, user_id: UUID) -> None:
        with self.get_session() as ctx:
            self.user_repo.delete(user_id=user_id, session=ctx)

    def get_user_profile(self, user_id: UUID) -> UserResponse:
        with self.get_session() as ctx:
            user = self.user_repo.get_by_id(user_id=user_id, session=ctx)
            if user is None:
                raise UserNotFoundException(user_id)

            return UserResponseProvider.from_user_db(user=user)


    def save_user_or_get_profile_from_yandex(
            self, yandex_sso: UserYandex, is_test_user: bool= False
    ) -> DBUser:
        with self.get_session() as ctx:
            user = self.user_repo.get_user_by_yandex_sso(
                yandex_id=yandex_sso.id, session=ctx
            )

            if user is None:
                user_id = self.user_repo.save_user_profile_from_yandex(
                    yandex_sso=yandex_sso, is_test_user=is_test_user, session=ctx
                )

            else:
                self.user_repo.update_user_profile_from_yandex(
                    yandex_sso=yandex_sso, user_id=user.id, session=ctx
                )
                user_id = user.id

            result = self.user_repo.get_by_id(
                user_id=user_id, session=ctx
            )
            if result is None:
                raise UserNotFoundException(user_id)


            return UserResponseProvider.from_user_db(user=result)

    def list_users(
            self
    ) -> list[Any]:
        with self.get_session() as ctx:
            users = self.user_repo.list_all(session=ctx)

            return [UserResponseProvider.from_user_db(user=user) for user in users]

    def get_user_profile_by_email(self, email: str):
        with self.get_session() as ctx:
            user = self.user_repo.get_by_email(email=email, session=ctx)
            if user is None:
                raise UserNotFoundByEmailException(email=email)
            return UserResponseProvider.from_user_db(user=user)
