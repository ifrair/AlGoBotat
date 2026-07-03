import pytest
import responses

from service.interfaces.auth_service_i import AuthServiceI
from service.schemes import LoginData, AuthType
from service.schemes import UserYandex


class TestAuthService:
    @pytest.mark.positive
    @responses.activate
    def test_login(
        self,
        auth_service: AuthServiceI,
        mocker,
        user_yandex: UserYandex,
        token_url,
        yandex_login_url,
    ):
        login_data = LoginData(auth_type=AuthType.YANDEX_SSO, data="some_code")

        responses.add(
            responses.POST,
            token_url,
            json={"access_token": "some_token"},
            status=200,
        )

        responses.add(
            responses.GET,
            yandex_login_url,
            json=user_yandex.model_dump(),
            status=200,
        )

        spy = mocker.spy(obj=auth_service.yandex_sso_service, name="fetch_user_data")

        jwt_token = auth_service.login(sso_data=login_data)

        assert jwt_token
        assert spy.call_count == 1
