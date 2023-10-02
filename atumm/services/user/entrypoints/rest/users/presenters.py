from atumm.core.types import AbstractPresenter
from atumm.services.user.domain.entities import User
from atumm.services.user.entrypoints.rest.users.responses import RegisterResponse


class UserPresenter(AbstractPresenter[User, RegisterResponse]):
    def present(self, user: User) -> RegisterResponse:
        return RegisterResponse(**user.dict())
