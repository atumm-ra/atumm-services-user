from typing import List

from atumm.core.entrypoints.rest.responses import RuntimeExceptionResponse
from atumm.extensions.di.resolver import LocalDepends
from atumm.services.user.domain.usecases.register import RegisterCommand
from atumm.services.user.entrypoints.rest.users.controllers import UserController
from atumm.services.user.entrypoints.rest.users.responses import (
    GetUsersResponse,
    RegisterResponse,
)
from fastapi import Query
from fastapi.routing import APIRouter
from fastapi_restful.cbv import cbv

router = APIRouter(prefix="/users")


@cbv(router)
class UserRouter:
    @property
    def controller(self) -> UserController:
        return LocalDepends(UserController)

    @router.post(
        "/",
        response_model=RegisterResponse,
        status_code=201,
        responses={
            "400": {"model": RuntimeExceptionResponse},
            "401": {"model": RuntimeExceptionResponse},
        },
    )
    async def create_user(self, command: RegisterCommand):
        return await self.controller.register_action(command)

    @router.get(
        "/",
        response_model=List[GetUsersResponse],
        response_model_exclude={"id"},
        responses={
            "400": {"model": RuntimeExceptionResponse},
            "401": {"model": RuntimeExceptionResponse},
        },
    )
    async def get_user_list(
        self,
        start_from: int = Query(0, description="Slice from"),
        num_items: int = Query(10, description="Number of items to return"),
    ):
        return await self.controller.get_user_list_action(
            start=start_from, limit=num_items
        )


user_router = router
