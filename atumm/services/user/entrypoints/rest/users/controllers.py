from typing import List, Optional

from atumm.core.exceptions import RuntimeException
from atumm.extensions.fastapi.schemas.current_user import CurrentUser
from atumm.extensions.services.tokenizer.base import BaseTokenizer
from atumm.services.user.dataproviders.beanie.models import User
from atumm.services.user.domain.usecases.get_user import (
    GetUserInfoQuery,
    GetUserInfoUseCase,
)
from atumm.services.user.domain.usecases.get_users import GetUsersQuery, GetUsersUseCase
from atumm.services.user.domain.usecases.register import (
    RegisterCommand,
    RegisterUseCase,
)
from atumm.services.user.entrypoints.rest.users.presenters import UserPresenter
from atumm.services.user.entrypoints.rest.users.responses import (
    GetUsersResponse,
    RegisterResponse,
)
from injector import inject


class UserController:
    @inject
    def __init__(
        self,
        register_usecase: RegisterUseCase,
        get_user_info_usecase: GetUserInfoUseCase,
        get_users_usecase: GetUsersUseCase,
    ):
        self.register_usecase = register_usecase
        self.get_user_info_usecase = get_user_info_usecase
        self.get_users_usecase = get_users_usecase

    async def register_action(self, command: RegisterCommand) -> User:
        return await self.register_usecase.execute(command)

    async def get_user_action(self, start: int, limit: int) -> List[User]:
        return await self.get_users_usecase.execute(
            GetUsersQuery(limit=limit, start=start)
        )


class UserController:
    @inject
    def __init__(
        self,
        register_usecase: RegisterUseCase,
        get_user_info_usecase: GetUserInfoUseCase,
        get_users_usecase: GetUsersUseCase,
        presenter: UserPresenter,
        tokenizer: BaseTokenizer,
    ):
        self.register_usecase = register_usecase
        self.get_user_info_usecase = get_user_info_usecase
        self.get_users_usecase = get_users_usecase
        self.presenter = presenter
        self.tokenizer = tokenizer

    async def register_action(self, command: RegisterCommand) -> RegisterResponse:
        user = await self.register_usecase.execute(command)
        return self.presenter.present(user)

    async def get_user_info_action(
        self, user: Optional[CurrentUser]
    ) -> RegisterResponse:
        if not user:
            raise RuntimeException(401, "Authentication failed")
        return await self.presenter.present(
            self.get_user_info_usecase.execute(GetUserInfoQuery(email=user.email))
        )

    async def get_user_list_action(
        self, start: int, limit: int
    ) -> List[GetUsersResponse]:
        users = await self.get_users_usecase.execute(
            GetUsersQuery(limit=limit, start=start)
        )
        return self.presenter.present_list(users)
