from injector import Module, provider, singleton

from src.connections.pgsql.connection import PostgreSQLClient
from src.connections.sqlite.connection import SQLiteClient


class ClientsModule(Module):
    @singleton
    @provider
    def provide_postgresql_client(self) -> PostgreSQLClient:
        return PostgreSQLClient()

    @singleton
    @provider
    def provide_sqlite_base(self) -> SQLiteClient:
        return SQLiteClient()