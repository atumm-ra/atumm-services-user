from typing import Dict, Optional

from atumm.core.types import Command, CommandUseCase
from atumm.extensions.services.tokenizer.base import BaseTokenizer
from atumm.services.user.domain.exceptions import (
    AccountLockedException,
    PasswordsDoNotMatchException,
    UserNotFoundException,
)
from atumm.services.user.domain.repositories import AbstractUserRepo
from atumm.services.user.domain.services import PasswordHasher
from injector import inject


class LoginCommand(Command):
    email: str
    password: str
    device_id: Optional[str] = None


class LoginUseCase(CommandUseCase[LoginCommand]):
    @inject
    def __init__(
        self,
        user_repo: AbstractUserRepo,
        tokenizer: BaseTokenizer,
        hasher: PasswordHasher,
    ):
        self.repo = user_repo
        self.tokenizer = tokenizer
        self.hasher = hasher

    async def execute(self, command: LoginCommand) -> Dict[str, str]:
        user = await self.repo.find_by_email(email=command.email)
        if not user:
            raise UserNotFoundException()

        if user.is_locked():
            raise AccountLockedException()

        if not self.hasher.is_password_valid(
            command.password, user.password, user.salt
        ):
            raise PasswordsDoNotMatchException

        if user.device_id is None:
            user.device_id = command.device_id
            await self.repo.save(user)

        token = self.tokenizer.encode(
            payload={"sub": str(user.email), "user_id": str(user.id), "type": "access"}
        )
        refresh_token = self.tokenizer.encode(
            payload={"sub": "refresh", "type": "refresh"}
        )
        return {"token": token, "refresh_token": refresh_token}
