from atumm.services.user.domain.models import UserModel
from beanie import Document
from pymongo import IndexModel


class User(Document, UserModel):
    class Beanie:
        document_model_name = "users"

    class Settings:
        indexes = [
            IndexModel("email", unique=True),
            IndexModel("username", unique=True),
        ]
        is_root = True
