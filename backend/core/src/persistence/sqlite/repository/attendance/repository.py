import json
from typing import List, Optional
from uuid import UUID

from src.connections.sqlite.base import SqliteBase
from src.connections.sqlite.connection import SQLiteClient
from src.domains.attendances.repository import AttendanceOfflineRepository
from src.dtos.attendance.create import CreateAttendanceMedicationDTO
from src.dtos.attendance.read import Attendance


class AttendanceRepositorySQLite(SqliteBase, AttendanceOfflineRepository):
    def __init__(self, db: SQLiteClient) -> None:
        super().__init__(db)

    async def save_attendance_offline(
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
        """
        Saves the attendance offline, queries local DB for names to avoid empty fields,
        and returns the full domain entity.
        """
        record_id = str(id)
        now = self._now_sp()

        meds_list = []
        if medications:
            for med in medications:
                if hasattr(med, "model_dump"):
                    meds_list.append(med.model_dump(mode="json"))
                elif isinstance(med, dict):
                    meds_list.append(med)

        meds_json = json.dumps(meds_list, default=str)

        with self.sqlite.get_connection() as conn:
            # Busca o nome do paciente (ajuste 'name' se a coluna for diferente, ex: 'full_name')
            cur_patient = conn.execute("SELECT name FROM patients WHERE id = ?", (str(patient_id),))
            row_patient = cur_patient.fetchone()
            patient_name = row_patient[0] if row_patient else "Paciente não sincronizado"

            # Busca o nome do profissional (ajuste 'name' se a coluna for diferente)
            cur_prof = conn.execute("SELECT name FROM professionals WHERE id = ?", (str(professional_id),))
            row_prof = cur_prof.fetchone()
            professional_name = row_prof[0] if row_prof else "Profissional não sincronizado"

            conn.execute(
                """
                INSERT INTO attendances 
                (id, medical_record_id, professional_id, pressure, heart_rate, consciousness_level, triage_protocol, notes, created_at, medications_json, is_synced)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
                """,
                (
                    record_id,
                    str(medical_record_id),
                    str(professional_id),
                    pressure,
                    heart_rate,
                    consciousness_level,
                    triage_protocol,
                    notes,
                    now,
                    meds_json,
                ),
            )
            self._log_offline_action(
                conn, str(professional_id), "POST", "/core/usecases/attendance/"
            )
            conn.commit()

        return Attendance(
            id=id,
            medical_record_id=medical_record_id,
            professional_id=professional_id,
            patient_id=patient_id,
            patient_name=patient_name,
            professional_name=professional_name,
            pressure=pressure,
            heart_rate=heart_rate,
            consciousness_level=consciousness_level,
            triage_protocol=triage_protocol,
            notes=notes,
            created_at=now
        )