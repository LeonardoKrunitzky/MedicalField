from datetime import datetime
from pathlib import Path
from uuid import UUID

from src.connections.pgsql.base import PostgresqlBase
from src.connections.pgsql.connection import PostgreSQLClient
from src.domains.patients.entity import Patient
from src.domains.patients.repository import PatientRepository
from src.persistence.pgsql.repository.medication.repository import _QUERIES_DIR

_QUERIES_DIR = Path(__file__).resolve().parent / "queries"
CREATE_QUERY = (_QUERIES_DIR / "create.sql").read_text(encoding="utf-8")
FETCH_QUERY = (_QUERIES_DIR / "fetch.sql").read_text(encoding="utf-8")
FETCH_BY_ID_QUERY = (_QUERIES_DIR / "fetch_by_id.sql").read_text(encoding="utf-8")


class PatientRepositoryPostgreSQL(PostgresqlBase, PatientRepository):
    def __init__(self, db: PostgreSQLClient):
        super().__init__(db)

    async def fetch_all(self) -> list[Patient]:
        rows = await self._execute_query(FETCH_QUERY)

        if not rows:
            return []

        return rows

    async def fetch_by_id(self, patient_id: UUID) -> Patient:
        rows = await self._execute_query(
            query=FETCH_BY_ID_QUERY, params={"patient_id": patient_id}
        )

        if not rows:
            return None

        return rows[0]

    async def create(self, id: UUID, name: str, document: str, created_at: datetime) -> Patient:
        return await self._execute_command(
            query=CREATE_QUERY, params={"id": id, "name": name, "document": document, "created_at": created_at}
        )

        