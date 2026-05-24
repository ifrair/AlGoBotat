from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class JWTUser(BaseModel):
    user_id: str
    role: str


class User(BaseModel):
    id: UUID | str | None
    username: str | None
    first_name: str | None
    last_name: str | None
    bio: str | None
    email: str
    created_at: datetime | str
    updated_at: datetime | str

    is_test_user: bool
    is_banned: bool

