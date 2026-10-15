from pathlib import Path
from typing import List, Optional
from uuid import UUID

from src.connections.pgsql.base import PostgresqlBase
from src.connections.pgsql.connection import PostgreSQLClient
from src.domains.attendances.repository import AttendanceRepository
from src.dtos.attendance.create import CreateAttendanceMedicationDTO
from src.dtos.attendance.read import Attendance

QUERYS_DIR = Path(__file__).resolve().parent / "queries"
CREATE_QUERY = (QUERYS_DIR / "create.sql").read_text(encoding="utf-8")
FETCH_QUERY = (QUERYS_DIR / "fetch.sql").read_text(encoding="utf-8")
FETCH_BY_PATIENT_QUERY = (QUERYS_DIR / "fetch_by_patient.sql").read_text(
    encoding="utf-8"
)


class AttendanceRepositoryPostgreSQL(PostgresqlBase, AttendanceRepository):

    def __init__(self, db: PostgreSQLClient) -> None:
        super().__init__(db)

    async def create(
        self,
        id: UUID,
        medical_record_id: UUID,
        professional_id: UUID,
        patient_id: UUID,
        pressure: str,
        heart_rate: int,
        consciousness_level: int,
        triage_protocol: str,
        notes: Optional[str],
        medications: Optional[List[CreateAttendanceMedicationDTO]],
    ) -> Attendance:
        rows = await self._execute_query(
            CREATE_QUERY,
            params={
                "id": id,
                "medical_record_id": medical_record_id,
                "professional_id": professional_id,
                "patient_id": patient_id,
                "pressure": pressure,
                "heart_rate": heart_rate,
                "consciousness_level": consciousness_level,
                "triage_protocol": triage_protocol,
                "notes": notes,
                "medications": medications,
            },
        )

        if not rows:
            return None

        return rows[0]

    async def fetch_all(self) -> list[Attendance]:
        rows = await self._execute_query(FETCH_QUERY)

        if not rows:
            return []

        return rows

    async def fetch_by_patient(self, patient_id: UUID) -> list[Attendance]:
        rows = await self._execute_query(
            FETCH_BY_PATIENT_QUERY, params={"patient_id": patient_id}
        )

        if not rows:
            return []

        return rows