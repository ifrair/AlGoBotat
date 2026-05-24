from __future__ import annotations

import dataclasses
from datetime import date, datetime, timedelta
from enum import StrEnum, auto
from typing import Callable
from uuid import UUID

from pydantic import BaseModel


class Base(BaseModel):
    pass


class User(Base):
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

