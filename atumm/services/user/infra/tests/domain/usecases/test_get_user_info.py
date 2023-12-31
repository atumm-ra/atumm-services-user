from unittest.mock import AsyncMock

import pytest
from atumm.services.user.domain.entities import User
from atumm.services.user.domain.usecases.get_user import (
    GetUserInfoQuery,
    GetUserInfoUseCase,
)
from faker import Faker


class TestGetUserInfoUseCase:
    faker = Faker()

    @pytest.mark.anyio
    async def test_get_user_info(self):
        email = self.faker.email()
        password = self.faker.password()
        user = User(email=email, password=password)

        user_repo = AsyncMock()
        user_repo.find_by_email.return_value = user

        get_user_info_query = GetUserInfoQuery(email=email)
        get_user_info_use_case = GetUserInfoUseCase(user_repo)

        returned_user = await get_user_info_use_case.execute(get_user_info_query)

        user_repo.find_by_email.assert_called_once_with(email)
        assert returned_user == user
