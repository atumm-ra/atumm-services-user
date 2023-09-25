from unittest.mock import AsyncMock

import pytest
from atumm.extensions.services.tokenizer.jwt_tokenizer import JWTTokenizer
from atumm.services.user.domain.models import UserModel
from atumm.services.user.domain.services import PasswordHasher
from atumm.services.user.domain.usecases.login import LoginCommand, LoginUseCase
from faker import Faker


class TestLoginUseCase:
    faker = Faker()

    @pytest.mark.anyio
    async def test_login(self):
        email = self.faker.email()
        password = self.faker.password()
        device_id = self.faker.uuid4()
        hasher = PasswordHasher("pass_key")
        salt = hasher.generate_salt()
        user = UserModel(
            email=email,
            password=hasher.hash_password(password, salt),
            device_id=device_id,
        )
        user.salt = salt

        user_repo = AsyncMock()
        user_repo.find_by_email.return_value = user

        login_command = LoginCommand(
            email=email, password=password, device_id=device_id
        )
        login_use_case = LoginUseCase(
            user_repo, JWTTokenizer(self.faker.word(), 3600), hasher
        )

        tokens = await login_use_case.execute(login_command)
        assert "token" in tokens.keys()
        assert "refresh_token" in tokens.keys()
