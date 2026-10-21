from datetime import datetime
from pathlib import Path
from uuid import UUID

from src.connections.pgsql.base import PostgresqlBase
from src.connections.pgsql.connection import PostgreSQLClient
from src.domains.medical_records.entity import MedicalRecord
from src.domains.medical_records.repository import MedicalRecordRepository

_QUERIES_DIR = Path(__file__).resolve().parent / "queries"
FETCH_QUERY = (_QUERIES_DIR / "fetch.sql").read_text(encoding="utf-8")
FETCH_BY_PATIENT_QUERY = (_QUERIES_DIR / "fetch_by_patient.sql").read_text(
    encoding="utf-8"
)
FETCH_BY_ID_QUERY = (_QUERIES_DIR / "fetch_by_id.sql").read_text(encoding="utf-8")
CREATE_QUERY = (_QUERIES_DIR / "create.sql").read_text(encoding="utf-8")


class MedicalRecordRepositoryPostgreSQL(PostgresqlBase, MedicalRecordRepository):

    def __init__(self, db: PostgreSQLClient) -> None:
        super().__init__(db)

    async def fetch_all(self) -> list[MedicalRecord]:
        rows = await self._execute_query(FETCH_QUERY)

        if not rows:
            return []

        return rows

    async def fetch_by_patient(self, patient_id: UUID) -> MedicalRecord:
        rows = await self._execute_query(
            FETCH_BY_PATIENT_QUERY, params={"patient_id": patient_id}
        )
        
        if not rows:
            return []
        
        return rows[0]

    async def fetch_by_id(self, medical_record_id: UUID) -> MedicalRecord:
        rows = await self._execute_query(
            FETCH_BY_ID_QUERY, params={"medical_record_id": medical_record_id}
        )
        
        if not rows:
            return []
        
        return rows[0]

    async def create(
        self,
        id: UUID,
        patient_id: UUID,
        blood_type: str,
        known_allergies: str,
        chronic_conditions: str,
        emergency_contact: str,
        created_at: datetime
    ) -> MedicalRecord:
        return await self._execute_command(
            query=CREATE_QUERY,
            params={
                "id": id,
                "patient_id": patient_id,
                "blood_type": blood_type,
                "known_allergies": known_allergies,
                "chronic_conditions": chronic_conditions,
                "emergency_contact": emergency_contact,
                "created_at": created_at
            },
        )
