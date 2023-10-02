from atumm.extensions.config import Config
from atumm.services.user.dataproviders.beanie.repositories import UserRepo
from atumm.services.user.domain.repositories import UserRepositoryInterface
from atumm.services.user.domain.services import PasswordHasher
from injector import Module, provider, singleton


class PasswordHasherProvider(Module):
    @provider
    @singleton
    def provide(self, config: Config) -> PasswordHasher:
        return PasswordHasher(config.PASSWORD_KEY)


class UserRepoProvider(Module):
    @provider
    @singleton
    def provide(self, hasher: PasswordHasher) -> UserRepositoryInterface:
        return UserRepo(hasher)


user_providers = [PasswordHasherProvider, UserRepoProvider]
