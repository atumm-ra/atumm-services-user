from atumm.core.types import Command, CommandUseCase
from atumm.services.user.domain.exceptions import (
    DuplicateEmailOrUsernameException,
    PasswordsDoNotMatchException,
)
from atumm.services.user.domain.repositories import UserRepositoryInterface
from injector import inject
from pydantic import EmailStr, Field, FieldValidationInfo, field_validator


class RegisterCommand(Command):
    email: EmailStr = Field(..., description="Email")
    password1: str = Field(..., description="Password1")
    password2: str = Field(..., description="Password2")
    username: str = Field(..., description="username")

    @field_validator("password2", mode="before")
    def passwords_match(cls, password2: str, info: FieldValidationInfo) -> str:
        password1 = info.data.get("password1")
        if password1 is None:
            raise ValueError("password1 is required.")
        if password1 != password2:
            raise PasswordsDoNotMatchException("Passwords do not match!")
        return password2

    @field_validator("password1")
    def validate_password(cls, password: str, info: FieldValidationInfo) -> str:
        if password.__len__() < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one digit.")
        if not any(char.isupper() for char in password):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in password):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not any(char in "!@#$%^&*()_+-=[]{}|;:,.<>?/~`" for char in password):
            raise ValueError("Password must contain at least one special character.")
        return password


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
