from typing import List

import pymongo
from atumm.core.dataproviders.exceptions import DuplicateKeyException
from atumm.services.user.dataproviders.beanie.models import User
from atumm.services.user.domain.models import UserModel
from atumm.services.user.domain.repositories import AbstractUserRepo
from atumm.services.user.domain.services import PasswordHasher
from injector import inject


class UserRepo(AbstractUserRepo):
    @inject
    def __init__(self, hasher: PasswordHasher):
        self.hasher = hasher

    async def create(self, username: str, password: str, email: str) -> UserModel:
        user = User(email=email, password=password, username=username)
        user.salt = self.hasher.generate_salt()
        user.password = self.hasher.hash_password(user.password, user.salt)

        try:
            await User.insert_one(user)
        except pymongo.errors.DuplicateKeyError as e:
            raise DuplicateKeyException(e.details["keyValue"]) from e
        return user

    async def find_by_email(self, email: str) -> User:
        return await User.find_one({"email": email})

    async def find_all(self, start: int = 0, limit: int = 12) -> List[UserModel]:
        return await User.find().skip(start).to_list(limit)

    async def save(self, user: User) -> None:
        await user.save()
