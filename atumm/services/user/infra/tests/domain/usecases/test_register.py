from unittest.mock import AsyncMock

import pytest
from atumm.services.user.domain.entities import User
from atumm.services.user.domain.usecases.register import (
    RegisterCommand,
    RegisterUseCase,
)
from faker import Faker


class TestRegisterUseCase:
    faker = Faker()

    @pytest.mark.anyio
    async def test_register(self):
        email = self.faker.email()
        password = self.faker.password()
        username = self.faker.user_name()

        user = User(email=email, password=password, username=username)

        user_repo = AsyncMock()
        user_repo.find_by_email.return_value = None
        user_repo.create.return_value = user

        register_command = RegisterCommand(
            email=email, password1=password, password2=password, username=username
        )
        register_use_case = RegisterUseCase(user_repo)

        created_user = await register_use_case.execute(register_command)

        user_repo.create.assert_called_once_with(username, password, email)
        assert created_user.email == email
        assert created_user.username == username
