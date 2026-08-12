import random
import uuid
from contextlib import contextmanager
from typing import Any, Generator
from uuid import UUID

from loguru import logger
from sqlalchemy import select, update, delete, func, text
from sqlalchemy.orm import joinedload, Session

from db.engineer import DbEngine
from db.model import DBUser, DBUserYandexSSO
from service.schemes import UserYandex


class UserRepo:
    def __init__(self):
        self.db = DbEngine()

    @contextmanager
    def get_user_session(self, session: Session | None = None) -> Generator[Session, None, None]:
        if session is not None:
            yield session
        else:
            with self.db.get_session() as s:
                yield s

    def get_by_id(self, user_id: UUID, session: Session) -> DBUser | None:
        stmt = select(DBUser).where(DBUser.id == user_id)
        return session.execute(stmt).unique().scalar_one_or_none()

    def get_by_email(self, email: str, session: Session) -> DBUser | None:
        stmt = select(DBUser).where(DBUser.email == email)
        return session.execute(stmt).unique().scalar_one_or_none()

    def list_all(self, session: Session) -> list[DBUser]:
        stmt = select(DBUser)
        return list(session.scalars(stmt).all())

    def delete(self, user_id: UUID, session: Session) -> bool:
        stmt = select(DBUser).where(DBUser.id == user_id)
        user = session.execute(stmt).unique().scalar_one_or_none()

        if not user:
            logger.debug("User %s not found", user_id)
            return False

        session.delete(user)
        logger.info("User %s deleted", user_id)

        return True

    def set_banned(self, user_id: UUID, banned: bool, session: Session) -> DBUser:
        stmt = select(DBUser).where(DBUser.id == user_id)
        user = session.execute(stmt).unique().scalar_one_or_none()
        if not user:
            return None
        user.is_banned = banned
        session.flush()
        logger.info("User %s ban status set to %s", user_id, banned)

        return user

    def get_user_by_yandex_sso(self, yandex_id: int, session: Session) -> DBUser | None:
        stmt = (
            select(DBUser)
            .join(DBUserYandexSSO)
            .where(DBUserYandexSSO.yandex_id == yandex_id)
            .limit(1)
        )
        result = session.execute(stmt).unique().one_or_none()

        if result is not None:
            logger.info("User with yandex id %d found in db.", yandex_id)
            return result[0]
        else:
            logger.error("User with yandex id %d not found in db.", yandex_id)
            return None

    def save_user_profile_from_yandex(
        self,
        yandex_sso: "UserYandex",
        session: Session, is_test_user: bool = False
    ) -> UUID:
        logger.debug("Save user %s from Yandex sso to DB...", yandex_sso.login)

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
        session: Session, is_test_user: bool = False
    ) -> None:
        logger.debug("Updating user %s from Yandex sso...", yandex_sso.login)

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
        session.flush()

        yandex_user = DBUserYandexSSO(
            user_id=user_id,
            yandex_id=yandex_sso.id,
            default_email=yandex_sso.default_email,
            emails=yandex_sso.emails[:],
            login=yandex_sso.login,
        )
        session.merge(yandex_user)
        logger.info("Information from Yandex SSO %s updated in db.", yandex_sso)

    def generate_and_save_random_user(
            self,
            session: Session,
    ) -> UUID:
        user = DBUser(first_name="Coder", last_name="Roast", email="test@email.com",
                      is_test_user=True, username=str(uuid.uuid4()), photo_url="test_mock" )

        session.add(user)

        session.flush()

        return user.id

    def delete_test_users(self, session: Session):
        stmt = 'DELETE FROM "user" WHERE is_test_user'
        session.execute(text(stmt))

    async def get_random_user_id(
            self,
            is_test: bool | None,
            session: Session,
    ) -> UUID:
        pick_sql = text(f"""
            SELECT u.id
            FROM "user" u
            WHERE u.is_test_user = :is_test
            ORDER BY RANDOM()
            LIMIT 1
        """)
        result = session.execute(pick_sql, {
            "is_test": is_test,
        })
        return result.one_or_none()[0]
