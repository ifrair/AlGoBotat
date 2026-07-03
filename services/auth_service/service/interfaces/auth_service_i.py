from abc import ABC, abstractmethod

from service.schemes import LoginData


class AuthServiceI(ABC):
    @abstractmethod
    def login(self, sso_data: LoginData) -> str:
        pass
