from abc import abstractmethod
from typing import List, Protocol

from atumm.services.user.domain.entities import User


class UserRepositoryInterface(Protocol):
    async def create(self, username: str, password: str, email: str) -> User:
        ...

    async def find_by_email(self, email: str) -> User:
        ...

    async def find_all(self, start: int = 0, limit: int = 12) -> List[User]:
        ...

    async def save(self, user: User) -> None:
        ...
