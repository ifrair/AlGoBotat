from fastapi import APIRouter

from service.auth_service import AuthService
from service.schemes import LoginData

app = APIRouter(prefix="/api/v1/auth")
auth_service = AuthService()


@app.post(
    "/login",
    summary="Получение информации о пользователе для входа в систему",
    description="""Вход в систему как демо-пользователь без SSO.""",
)
async def login(sso_data: LoginData):
    jwt_token = auth_service.login(sso_data=sso_data)

    return jwt_token
