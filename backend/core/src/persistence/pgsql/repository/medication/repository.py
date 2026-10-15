from pathlib import Path

from src.connections.pgsql.base import PostgresqlBase
from src.connections.pgsql.connection import PostgreSQLClient
from src.domains.medication.repository import MedicationRepository
from src.dtos.medication.read import Medication, MedicationByAttendance

_QUERIES_DIR = Path(__file__).resolve().parent / "queries"
FETCH_QUERY = (_QUERIES_DIR / "fetch.sql").read_text(
    encoding="utf-8"
)
FETCH_BY_ATTENDANCE_QUERY = (_QUERIES_DIR / "fetch_by_attendance.sql").read_text(
    encoding="utf-8"
)

class MedicationRepositoryPostgreSQL(PostgresqlBase, MedicationRepository):

    def __init__(self, db: PostgreSQLClient) -> None:
        super().__init__(db)

    async def fetch_all(self) -> list[Medication]:
        rows = await self._execute_query(query=FETCH_QUERY)
        if not rows:
            return []
           
        return rows 

    async def fetch_by_attendance(self, attendance_id: int) -> list[MedicationByAttendance]:
        rows = await self._execute_query(
            query=FETCH_BY_ATTENDANCE_QUERY, params={"attendance_id": attendance_id}
        )

        if not rows:
            return []

        return rows