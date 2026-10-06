from injector import (Module, provide, singleton)

from backend.core.src.connections.pgsql.connection import PostgreSQLClient
from backend.core.src.domains.authentication.repository import AuthenticationRepository


class DomainModule(Module):
    @provide
    @singleton
    def provide_authentication_repository(self, client: PostgreSQLClient) -> AuthenticationRepository:
        return AuthenticationRepositoryPostgreSQL(client=client)