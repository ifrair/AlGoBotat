from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from commons.constants import UserRole


class JWTUser(BaseModel):
    user_id: str
    role: str


class User(BaseModel):
    id: UUID
    yandex_id: str | None = None
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    email: str

    role: UserRole = UserRole.USER

    created_at: datetime | str
    updated_at: datetime | str

    is_test_user: bool = False
    is_banned: bool = False
