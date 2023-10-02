from typing import List

import pymongo
from atumm.core.dataproviders.exceptions import DuplicateKeyException
from atumm.services.user.dataproviders.beanie.entities import UserDocument
from atumm.services.user.domain.entities import User
from atumm.services.user.domain.repositories import UserRepositoryInterface
from atumm.services.user.domain.services import PasswordHasher
from injector import inject
from atumm.extensions.beanie.transformer import BeanieTransformer

class UserTransformer(BeanieTransformer):
    domain_entity: User
    beanie_entity: UserDocument

class UserRepo(UserRepositoryInterface):
    @inject
    def __init__(self, hasher: PasswordHasher, transformer: UserTransformer):
        self.hasher = hasher
        self.transformer = transformer

    async def create(self, username: str, password: str, email: str) -> User:
        user = UserDocument(email=email, password=password, username=username)
        user.salt = self.hasher.generate_salt()
        user.password = self.hasher.hash_password(user.password, user.salt)

        try:
            await UserDocument.insert_one(user)
        except pymongo.errors.DuplicateKeyError as e:
            raise DuplicateKeyException(e.details["keyValue"]) from e
        return self.transformer.to_domain_entity(user)

    async def find_by_email(self, email: str) -> User:
        user_doc = await UserDocument.find_one({"email": email})
        return self.transformer.to_domain_entity(user_doc)

    async def find_all(self, start: int = 0, limit: int = 12) -> List[User]:
        user_docs = await UserDocument.find().skip(start).to_list(limit)
        return [self.transformer.to_domain_entity(user_doc) for user_doc in user_docs]

    async def save(self, user: User) -> None:
        await self.transformer.to_beanie_entity(user).save()
