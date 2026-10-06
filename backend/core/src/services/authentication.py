from injector import inject

from backend.core.src.domains.authentication.repository import AuthenticationRepository

class AuthenticationServices:
    @inject
    def __init__(self, repository: AuthenticationRepository):
        self._repository = repository

    async def login(self, username: str, password: str):
        return await self._repository.login(username, password)