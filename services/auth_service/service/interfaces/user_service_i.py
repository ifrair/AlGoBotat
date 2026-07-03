import dataclasses
from abc import ABC, abstractmethod

from service.model import User
from service.schemes import UserYandex


@dataclasses.dataclass
class UserServiceI(ABC):
    @abstractmethod
    def get_or_save_user_by_yandex_sso(
        self, yandex_sso: UserYandex, is_test_user: bool = False
    ) -> User:
        pass
