from enum import StrEnum

from pydantic import BaseModel, EmailStr
import email_validator


class UserYandex(BaseModel):
    id: int
    login: str
    default_email: EmailStr
    emails: list[EmailStr] = []

    # "Full Access" fields using the | None syntax
    real_name: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    display_name: str | None = None
    birthday: str | None = None
    default_phone: dict | None = None
    default_avatar_id: str | None = None

    def __hash__(self):
        return hash(
            (type(self),) + tuple(getattr(self, f) for f in self.model_fields.keys())
        )

    def __eq__(self, other):
        return hash(self) == hash(other)


# We can't use auto here as far as it generates const in lower symbols regime
class AuthType(StrEnum):
    YANDEX_SSO = "YANDEX_SSO"


class LoginData(BaseModel):
    auth_type: AuthType
    data: str
