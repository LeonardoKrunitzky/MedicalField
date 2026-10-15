from typing import List, Any, Mapping
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.connections.pgsql.connection import PostgreSQLClient

class PostgresqlBase:
    """
    Base for repositories using raw SQL in an async context.
    """
    def __init__(self, client: PostgreSQLClient):
        """
        Initialize with the async postgres client.
        """
        self.client = client

    async def _execute_query(self, query: str, params: dict = None) -> List[Mapping[str, Any]]:
        """
        Executes SELECT queries and returns result mappings asynchronously.
        """
        try:
            async with self.client.session() as session:
                result = await session.execute(text(query), params or {})
                return result.mappings().all()
        except SQLAlchemyError as exc:
            raise RuntimeError(f"Database query failed: {str(exc)}") from exc

    async def _execute_command(self, query: str, params: dict = None) -> int:
        """
        Executes UPDATE, INSERT, DELETE and returns rowcount asynchronously.
        """
        try:
            async with self.client.session() as session:
                result = await session.execute(text(query), params or {})
                return result.rowcount
        except SQLAlchemyError as exc:
            raise RuntimeError(f"Database command failed: {str(exc)}") from exc