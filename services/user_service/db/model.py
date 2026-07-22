import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    Column,
    func,
    ForeignKey,
    String,
    TIMESTAMP,
    Boolean,
    BigInteger,
    Float,
    JSON,
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import declarative_base, relationship

if TYPE_CHECKING:
    pass
else:

    def dataclass_sql(cls):
        return cls


Base = declarative_base()


class UUIDMixin:
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.gen_random_uuid(),
    )


# =============== Main Models ===============
class DBUser(UUIDMixin, Base):
    __tablename__ = "user"

    username = Column(String(64))
    first_name = Column(String(64))
    last_name = Column(String(64))
    bio = Column(String(4096), nullable=True)
    photo_url = Column(String(256), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(
        TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    yandex_sso = relationship(
        "DBUserYandexSSO",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    course_assignments = relationship(
        "DBCourseAssignment",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    is_banned = Column(Boolean, server_default="False")
    is_test_user = Column(Boolean, server_default="False")
    email = Column(String(64))
    role = Column(String(16), server_default="USER")
    comment =Column(String(16), server_default="")


class DBUserYandexSSO(Base):
    __tablename__ = "user_yandex_sso"

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"))
    yandex_id = Column(BigInteger, primary_key=True)
    default_email = Column(String(64), nullable=False)

    default_avatar_id = Column(String(128), nullable=True)
    emails = Column(ARRAY(String), nullable=True)
    login = Column(String(64), nullable=True)

    user = relationship("DBUser", back_populates="yandex_sso")


class DBCourseAssignment(UUIDMixin, Base):
    __tablename__ = "course_assignment"

    course_id = Column(UUID(as_uuid=True), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(32), server_default="uncompleted")
    progress_percentage = Column(Float, server_default="0")
    progress = Column(JSON, server_default="{}")

    user = relationship("DBUser", back_populates="course_assignments")
