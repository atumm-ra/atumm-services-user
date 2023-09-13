from atumm.core.infra.config import Config, configure
from pydantic.fields import Field


@configure
class UserConfig(Config):
    JWT_SECRET_KEY: str = Field(...)
    JWT_ALGORITHM: str = Field(...)

    PASSWORD_KEY: str = Field(...)
