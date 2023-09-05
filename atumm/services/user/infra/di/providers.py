from atumm.core.infra.config import Config
from injector import Binder, Module, singleton

from atumm.services.user.dataproviders.beanie.repositories import UserRepo
from atumm.services.user.domain.repositories import AbstractUserRepo
from atumm.services.user.domain.services import PasswordHasher


class PasswordHasherProvider(Module):
    def configure(self, binder: Binder):
        binder.bind(
            interface=PasswordHasher,
            to=PasswordHasher(self.__injector__.get(Config).PASSWORD_KEY),
            scope=singleton,
        )


user_providers = [PasswordHasherProvider]
