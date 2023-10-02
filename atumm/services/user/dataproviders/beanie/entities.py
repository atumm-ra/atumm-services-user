from atumm.services.user.domain.entities import User
from beanie import Document
from pymongo import IndexModel


class UserDocument(Document, User):
    class Beanie:
        document_model_name = "users"

    class Settings:
        indexes = [
            IndexModel("email", unique=True),
            IndexModel("username", unique=True),
        ]
        is_root = True
