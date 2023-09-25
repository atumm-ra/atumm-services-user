from atumm.extensions.buti.keys import AtummContainerKeys
from atumm.services.user.entrypoints.rest.tokens.routers import tokens_router
from atumm.services.user.entrypoints.rest.users.routers import user_router
from buti import BootableComponent, ButiStore
from fastapi import APIRouter, FastAPI
from injector import Injector


class UserServiceComponent(BootableComponent):
    def boot(self, object_store: ButiStore):
        app: FastAPI = object_store.get(AtummContainerKeys.app)
        injector_obj: Injector = object_store.get(AtummContainerKeys.injector)

        user_api_router = APIRouter()
        user_api_router.include_router(user_router, prefix="/api/v1", tags=["Users"])
        user_api_router.include_router(
            tokens_router, prefix="/api/v1", tags=["AuthTokens"]
        )
        app.include_router(user_api_router)
