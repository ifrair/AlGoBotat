import os
from http import HTTPStatus

import dotenv
import requests
from requests import Response

from service.exceptions import YandexDataError
from service.schemes import UserYandex

dotenv.load_dotenv()


class YandexSSOService:
    def __init__(self):
        self.client_id = os.getenv("YANDEX_CLIENT_ID")
        self.client_secret = os.getenv("YANDEX_CLIENT_SECRET")
        self.login_url = os.getenv("YANDEX_LOGIN_URL", "https://login.yandex.ru/info")
        self.token_url = os.getenv("YANDEX_TOKEN_URL", "https://oauth.yandex.com/token")

    def _exchange_code_for_token(self, code: str) -> str:
        response = requests.post(
            url=self.token_url,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            }
        )

        if response.status_code != HTTPStatus.OK:
            raise YandexDataError(f"Cannot exchange yandex code for yandex token:\n{response.json()}, {code}")

        access_token = response.json().get("access_token")

        return access_token

    def fetch_user_data(self, code: str) -> UserYandex:
        token = self._exchange_code_for_token(code=code)
        response = self._exchange_token_for_data(token)

        return UserYandex.model_validate(response.json())

    def _exchange_token_for_data(self, token: str) -> Response:
        headers = {"Authorization": f"OAuth {token}"}
        response = requests.get(
            url=self.login_url, params={"format": "json"}, headers=headers
        )

        if response.status_code != HTTPStatus.OK:
            raise YandexDataError(f"Cannot exchange yandex token for yandex data:\n{response.json()}")

        return response
