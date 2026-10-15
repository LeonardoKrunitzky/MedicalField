from pathlib import Path
from uuid import UUID

from src.domains.professional.entity import Professional
from src.connections.pgsql.base import PostgresqlBase
from src.connections.pgsql.connection import PostgreSQLClient
from src.domains.professional.repository import ProfessionalRepository
from src.dtos.professional.login import LoginResponseDTO

_QUERIES_DIR = Path(__file__).resolve().parent / "queries"
READ_BY_REGISTRATION_QUERY = (_QUERIES_DIR / "read_by_registration.sql").read_text(
    encoding="utf-8"
)


class ProfessionalRepositoryPostgreSQL(PostgresqlBase, ProfessionalRepository):

    def __init__(self, db: PostgreSQLClient) -> None:
        super().__init__(db)

    async def read_by_professional_registration(
        self, professional_registration: str
    ) -> Professional:
        rows = await self._execute_query(
            query=READ_BY_REGISTRATION_QUERY,
            params={"professional_registration": professional_registration},
        )

        if not rows:
            return None

        return rows[0]