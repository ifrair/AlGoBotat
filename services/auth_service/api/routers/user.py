import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Query, Response, UploadFile
from starlette.responses import JSONResponse

from services.auth_service.db.model import DBUser
from services.auth_service.service.schemes import LoginData
from services.auth_service.service.user_service import UserService
from services.auth_service.service.yandex_sso_service import YandexSSOService

app = APIRouter(prefix="/api/v1/auth")
user_service=UserService()


@app.post(
    "/login",
    summary="Получение информации о пользователе для входа в систему",
    description="""Вход в систему как демо-пользователь без SSO."""
)
async def login(sso_data: LoginData):
    user = user_service.save_user_or_get_profile_from_yandex(code=sso_data.data)

    return user.id