from atumm.core.types import Query, QueryUseCase
from atumm.services.user.dataproviders.beanie.entities import UserDocument
from atumm.services.user.domain.repositories import UserRepositoryInterface
from injector import inject
from pydantic import EmailStr


class GetUserInfoQuery(Query):
    email: EmailStr


class GetUserInfoUseCase(QueryUseCase[GetUserInfoQuery]):
    @inject
    def __init__(self, user_repo: UserRepositoryInterface):
        self.user_repo = user_repo

    async def execute(self, command: GetUserInfoQuery) -> UserDocument:
        user = await self.user_repo.find_by_email(command.email)
        return user
