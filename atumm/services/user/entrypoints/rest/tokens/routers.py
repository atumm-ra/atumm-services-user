from atumm.core.entrypoints.rest.responses import RuntimeExceptionResponse
from atumm.extensions.di.resolver import LocalDepends
from atumm.services.user.entrypoints.rest.tokens.controllers import TokensController
from atumm.services.user.entrypoints.rest.tokens.requests import (
    LoginRequest,
    RefreshTokenRequest,
)
from atumm.services.user.entrypoints.rest.tokens.responses import (
    AuthenticatedTokensResponse,
)
from fastapi.routing import APIRouter
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter
from injector import inject

router = APIRouter(prefix="/tokens")


@cbv(router)
class TokensRouter:
    @property
    def controller(self) -> TokensController:
        return LocalDepends(TokensController)

    @router.post(
        "/refresh",
        responses={
            "200": {"model": AuthenticatedTokensResponse},
            "400": {"model": RuntimeExceptionResponse},
            "401": {"model": RuntimeExceptionResponse},
        },
    )
    async def refresh_token(
        self, request: RefreshTokenRequest
    ) -> AuthenticatedTokensResponse:
        return await self.controller.refresh_token(request)

    @router.post(
        "/access",
        responses={
            "200": {"model": AuthenticatedTokensResponse},
            "401": {"model": RuntimeExceptionResponse},
            "404": {"model": RuntimeExceptionResponse},
        },
    )
    async def login(self, request: LoginRequest) -> AuthenticatedTokensResponse:
        return await self.controller.login(request)


tokens_router = router
