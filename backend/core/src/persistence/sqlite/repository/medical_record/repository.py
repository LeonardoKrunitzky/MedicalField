from datetime import datetime
from typing import Optional
from uuid import UUID

from src.connections.sqlite.base import SqliteBase
from src.connections.sqlite.connection import SQLiteClient
from src.domains.medical_records.repository import MedicalRecordOfflineRepository                             


class MedicalRecordRepositorySQLite(SqliteBase, MedicalRecordOfflineRepository):
    def __init__(self, db: SQLiteClient) -> None:
        super().__init__(db)

    async def save_medical_record_offline(
        self,
        id: UUID,
        patient_id: UUID,
        blood_type: Optional[str],
        known_allergies: Optional[str],
        chronic_conditions: Optional[str],
        emergency_contact: Optional[str],
        created_at: datetime
    ) -> dict:
        record_id = str(id)
        pat_id = str(patient_id)

        with self.sqlite.get_connection() as conn:
            conn.execute(
                """
                INSERT INTO medical_records 
                (id, patient_id, blood_type, known_allergies, chronic_conditions, emergency_contact, created_at, is_synced)
                VALUES (?, ?, ?, ?, ?, ?, ?, 0)
                """,
                (
                    record_id,
                    pat_id,
                    blood_type,
                    known_allergies,
                    chronic_conditions,
                    emergency_contact,
                    created_at,
                ),
            )
            
            conn.commit()

        return {
            "id": id,
            "patient_id": patient_id,
            "blood_type": blood_type,
            "known_allergies": known_allergies,
            "chronic_conditions": chronic_conditions,
            "emergency_contact": emergency_contact,
            "created_at": created_at
        }