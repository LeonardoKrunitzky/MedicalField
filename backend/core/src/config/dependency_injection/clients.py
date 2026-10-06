from injector import Module, provider, singleton

from src.connections.pgsql.connection import PostgreSQLClient


class ClientsModule(Module):
    @singleton
    @provider
    def provide_postgresql_client(self) -> PostgreSQLClient:
        return PostgreSQLClient()
