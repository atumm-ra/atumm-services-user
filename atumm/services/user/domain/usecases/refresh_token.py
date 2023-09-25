from typing import Dict

from atumm.core.types import Command, CommandUseCase
from atumm.extensions.services.tokenizer.base import BaseTokenizer
from atumm.services.user.domain.exceptions import InvalidRefreshSubject
from injector import inject


class RefreshTokenCommand(Command):
    token: str
    refresh_token: str


class RefreshTokenUseCase(CommandUseCase[RefreshTokenCommand]):
    @inject
    def __init__(self, tokenizer: BaseTokenizer):
        self.tokenizer = tokenizer

    async def execute(self, command: RefreshTokenCommand) -> Dict[str, str]:
        token_decoded = self.tokenizer.decode(token=command.token)

        refresh_token_decoded = self.tokenizer.decode(token=command.refresh_token)
        if refresh_token_decoded.get("sub") != "refresh":
            raise InvalidRefreshSubject()

        new_token = self.tokenizer.encode(
            payload={
                "user_id": token_decoded.get("user_id"),
                "sub": token_decoded.get("sub"),
            }
        )
        new_refresh_token = self.tokenizer.encode(payload={"sub": "refresh"})

        return {"token": new_token, "refresh_token": new_refresh_token}
