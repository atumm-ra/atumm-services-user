from abc import abstractmethod
from typing import List

from atumm.core.types import DataProvider
from atumm.services.user.domain.models import UserModel


class AbstractUserRepo(DataProvider):
    @abstractmethod
    async def create(self, username: str, password: str, email: str) -> UserModel:
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> UserModel:
        pass

    @abstractmethod
    async def find_all(self, start: int = 0, limit: int = 12) -> List[UserModel]:
        pass

    @abstractmethod
    async def save(self, user: UserModel) -> None:
        pass
