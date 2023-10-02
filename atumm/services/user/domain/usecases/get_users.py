from typing import List

from atumm.core.types import Query, QueryUseCase
from atumm.services.user.domain.entities import User
from atumm.services.user.domain.repositories import UserRepositoryInterface
from injector import inject


class GetUsersQuery(Query):
    start: int
    limit: int


class GetUsersUseCase(QueryUseCase[GetUsersQuery]):
    @inject
    def __init__(self, user_repo: UserRepositoryInterface):
        self.user_repo = user_repo

    async def execute(self, query: GetUsersQuery) -> List[User]:
        users = await self.user_repo.find_all(start=query.start, limit=query.limit)
        return users
