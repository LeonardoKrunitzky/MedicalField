from uuid import UUID

from src.connections.sqlite.base import SqliteBase
from src.connections.sqlite.connection import SQLiteClient
from src.domains.patients.repository import PatientOfflineRepository


class PatientRepositorySQLite(SqliteBase, PatientOfflineRepository):
    def __init__(self, db: SQLiteClient) -> None:
        super().__init__(db)

    async def save_patient_offline(
        self, id: UUID, name: str, document: str, professional_id: UUID
    ) -> dict:
        record_id = str(id)
        now = self._now_sp()

        with self.sqlite.get_connection() as conn:
            conn.execute(
                """
                INSERT INTO patients (id, name, document, created_at, is_synced)
                VALUES (?, ?, ?, ?, 0)
                """,
                (record_id, name, document, now),
            )
            self._log_offline_action(
                conn, str(professional_id), "POST", "/core/usecases/patient/"
            )
            conn.commit()

        return {
            "id": id,
            "name": name,
            "document": document,
            "created_at": now,
        }