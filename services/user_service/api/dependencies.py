from uuid import UUID

from fastapi import Header, HTTPException, Request

from commons.constants import UserRole


def get_current_user_id(
    x_user_id: str = Header(None, alias="X-User-ID"),
    x_user_role: str = Header(None, alias="X-User-Role"),
) -> tuple[UUID, str]:
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Missing X-User-ID header")
    try:
        user_id = UUID(x_user_id)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid X-User-ID header")
    role = x_user_role or UserRole.USER
    return user_id, role


def require_admin(
    x_user_role: str = Header(None, alias="X-User-Role"),
) -> None:
    if x_user_role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
