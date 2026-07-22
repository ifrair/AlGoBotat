from uuid import UUID

from fastapi import HTTPException


class UserNotFoundException(HTTPException):
    def __init__(
        self,
        user_id: UUID,
        detail="Не удалось найти пользователя {user_id} в базе данных!",
    ):
        super().__init__(
            status_code=404,
            detail=detail.format(
                user_id=user_id,
            ),
        )


class UserNotFoundByEmailException(HTTPException):
    def __init__(
        self,
        email: str,
        detail="Не удалось найти пользователя {email} в базе данных!",
    ):
        super().__init__(
            status_code=404,
            detail=detail.format(
                email=email,
            ),
        )


class AdminAccessRequired(HTTPException):
    def __init__(
        self,
        user_id: UUID,
        detail="Пользователь {user_id} не является администратором!",
    ):
        super().__init__(
            status_code=403,
            detail=detail.format(user_id=user_id),
        )


class UserBannedException(HTTPException):
    def __init__(
        self,
        user_id: UUID,
        detail="Пользователь {user_id} заблокирован!",
    ):
        super().__init__(
            status_code=403,
            detail=detail.format(user_id=user_id),
        )
