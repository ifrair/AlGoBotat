import dataclasses
from abc import ABC, abstractmethod

from loguru import logger

from service.model import JWTUser
from service.schemes import LoginData


class AuthServiceI(ABC):
    @abstractmethod
    def login(self, sso_data: LoginData) -> str:
        pass
