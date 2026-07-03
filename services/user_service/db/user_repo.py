from loguru import logger
from sqlalchemy import UUID, select

from service.schemes import UserYandex
from services.user_service.db.engineer import DbEngine
from services.user_service.db.model import DBUser, DBUserYandexSSO


class UserRepo:
    def __init__(self):
        self.db = DbEngine()

    def get_user_by_yandex_sso(self, yandex_id: int) -> DBUser | None:
        with self.db.get_session() as session:
            smt = (
                select(DBUser)
                .join(DBUserYandexSSO)
                .where(DBUserYandexSSO.yandex_id == yandex_id)
                .limit(1)
            )
            result = session.execute(smt).unique().one_or_none()

        if result is not None:
            logger.info(
                "User with yandex id %d found in db.",
                yandex_id,
            )
            return result[0]
        else:
            logger.error(
                "User with yadnex id %d not found in db.",
                yandex_id,
            )
            return None

    def save_user_profile_from_yandex(
        self,
        yandex_sso: UserYandex,
        is_test_user: bool = False,
    ) -> UUID:
        logger.debug(
            "Save user %s from Yandex sso to DB...",
            yandex_sso.login,
        )

        with self.db.get_session() as session:
            user = DBUser(
                first_name=yandex_sso.first_name or "",
                last_name=yandex_sso.last_name or "",
                username=yandex_sso.display_name,
                is_test_user=is_test_user,
                email=yandex_sso.default_email,
                photo_url=f"https://avatars.yandex.net/get-yapic/{yandex_sso.default_avatar_id}/islands-200",
            )

            session.add(user)
            session.flush()

            yandex_user = DBUserYandexSSO(
                user_id=user.id,
                yandex_id=yandex_sso.id,
                default_email=yandex_sso.default_email,
                emails=yandex_sso.emails[:],
                login=yandex_sso.login,
            )
            session.add(yandex_user)

            logger.info("Information from Yandex SSO %s has saved in db.", yandex_sso)

        return user.id

    def update_user_profile_from_yandex(
        self,
        yandex_sso: UserYandex,
        user_id: UUID,
        is_test_user: bool = False,
    ) -> UUID | None:
        logger.debug(
            "Обновление пользователя %s из Yandex sso из базы данных...",
            yandex_sso.login,
        )

        with self.db.get_session() as session:
            user = DBUser(
                id=user_id,
                first_name=yandex_sso.first_name or "",
                last_name=yandex_sso.last_name or "",
                username=yandex_sso.display_name,
                is_test_user=is_test_user,
                email=yandex_sso.default_email,
                photo_url=f"https://avatars.yandex.net/get-yapic/{yandex_sso.default_avatar_id}/islands-200",
            )
            session.merge(user)

            logger.info("Information from Yandex SSO %s updated in sso.", yandex_sso)

        return user.id
