from enum import StrEnum, auto
from typing import Optional
from uuid import UUID, uuid4

import bcrypt
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class StatusEnum(StrEnum):
    ACTIVE = auto()
    LOCKED = auto()
    DELETED = auto()


class UserModel(BaseModel):
    model_config = ConfigDict()

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: EmailStr = Field(str)
    password: str = Field(..., min_length=8, description="The user's hashed password")
    username: str = Field(
        str, min_length=3, max_length=255, description="The user's unique username"
    )
    is_admin: bool = Field(
        False, description="Indicates if the user has admin privileges"
    )
    salt: str = Field(default_factory=bcrypt.gensalt, description="password salt")
    status: StatusEnum = Field(StatusEnum.ACTIVE)

    first_name: Optional[str] = Field(
        None, min_length=1, max_length=255, description="The user's first name"
    )
    last_name: Optional[str] = Field(
        None, min_length=1, max_length=255, description="The user's last name"
    )
    device_id: Optional[str] = Field(None)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return value

    def lock(self):
        self.status = StatusEnum.LOCKED

    def is_locked(self) -> bool:
        return self.status == StatusEnum.LOCKED
