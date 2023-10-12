from __future__ import annotations
from atumm.core.types import Command, CommandUseCase
from atumm.services.user.domain.exceptions import (
    DuplicateEmailOrUsernameException,
    PasswordsDoNotMatchException,
)
from atumm.services.user.domain.repositories import UserRepositoryInterface
from injector import inject
from pydantic import EmailStr, Field, FieldValidationInfo, model_validator


class RegisterCommand(Command):
    email: EmailStr = Field(..., description="Email")
    password1: str = Field(..., description="Password1")
    password2: str = Field(..., description="Password2")
    username: str = Field(..., description="username")

    @model_validator(mode='after')
    def passwords_match(self) -> RegisterCommand:
        if self.password1 is None:
            raise ValueError("password1 is required.")
        if self.password1 != self.password2:
            raise PasswordsDoNotMatchException("Passwords do not match!")
        return self

    @model_validator(mode="after")
    def validate_password(self) -> User:
        password = self.password1
        if password.__len__() < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one digit.")
        if not any(char.isupper() for char in password):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in password):
            raise ValueError("Password must contain at least one lowercase letter.")
        if all(char not in "!@#$%^&*()_+-=[]{}|;:,.<>?/~`" for char in password):
            raise ValueError("Password must contain at least one special character.")
        return self


class RegisterUseCase(CommandUseCase[RegisterCommand]):
    @inject
    def __init__(self, user_repo: UserRepositoryInterface):
        self.user_repo = user_repo

    async def execute(self, command: RegisterCommand):
        does_exist = await self.user_repo.find_by_email(command.email)

        if does_exist:
            raise DuplicateEmailOrUsernameException

        return await self.user_repo.create(
            command.username, command.password1, command.email
        )
