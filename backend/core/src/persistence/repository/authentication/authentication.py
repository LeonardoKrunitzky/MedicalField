from pathlib import Path

from injector import inject

from backend.core.src.connections.pgsql.base import PostgresqlBasePort
from backend.core.src.connections.pgsql.connection import PostgreSQLClient
from backend.core.src.domains.authentication.repository import AuthenticationRepository
from backend.core.src.dtos.authentication.login import LoginResponseDTO


class AuthenticationRepositoryPostgreSQL(PostgresqlBasePort, AuthenticationRepository):

    @inject
    def __init__(self, client: PostgreSQLClient) -> None:
        super().__init__(client)

    async def login(self, username: str, password: str) -> LoginResponseDTO | None:
        sql_path = Path("./queries/login.sql")
        query_str = sql_path.read_text(encoding="utf-8")
        
        rows = await self.client._execute_query(
            query_str, params={"username": username, "password": password}
        )

        return LoginResponseDTO(access_token=rows[0]) if rows else None