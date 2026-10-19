import json
import os
from typing import Any
from uuid import UUID, uuid4
import httpx
from injector import inject
from pydantic import BaseModel

from src.connections.sqlite.base import SqliteBase
from src.connections.sqlite.connection import SQLiteClient
from src.domains.professional.repository import ProfessionalRepository
from src.domains.sync.repository import SyncRepository
from src.domains.patients.repository import PatientRepository
from src.domains.medical_records.repository import MedicalRecordRepository
from src.domains.attendances.repository import AttendanceRepository
from src.domains.medication.repository import MedicationRepository
from src.strategies.sync_strategy import LatestTimestampStrategy


class SyncRepositorySQLite(SqliteBase, SyncRepository):

    def __init__(
        self,
        db: SQLiteClient,
        patient_repo: PatientRepository,
        medical_record_repo: MedicalRecordRepository,
        attendance_repo: AttendanceRepository,
        medication_repo: MedicationRepository,
        professional_repo: ProfessionalRepository,
    ) -> None:
        super().__init__(db)
        self.patient_repo = patient_repo
        self.medical_record_repo = medical_record_repo
        self.attendance_repo = attendance_repo
        self.medication_repo = medication_repo
        self.professional_repo = professional_repo
        self.strategy = LatestTimestampStrategy()
        self.go_logs_url = os.getenv("TRACING_URL")

    def _to_dict(self, item: Any) -> dict:
        """Converte Pydantic BaseModel, RowMapping do SQLAlchemy ou dict em dict puro."""
        if isinstance(item, dict):
            return item
        if isinstance(item, BaseModel) or hasattr(item, "model_dump"):
            return item.model_dump()
        if hasattr(item, "_mapping"):
            return dict(item._mapping)
        try:
            return dict(item)
        except Exception:
            return vars(item)

    async def pull_from_database(self) -> dict:
        try:
            medications = await self.medication_repo.fetch_all()
            patients = await self.patient_repo.fetch_all()
            records = await self.medical_record_repo.fetch_all()
            attendances = await self.attendance_repo.fetch_all()
            professionals = await self.professional_repo.fetch_all()
            with self.sqlite.get_connection() as conn:
                cursor = conn.cursor()

                for med_dict in medications:
                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO medications (id, name, standard_dosage, created_at)
                        VALUES (?, ?, ?, ?)
                        """,
                        (
                            str(med_dict["id"]),
                            med_dict["name"],
                            med_dict.get("standard_dosage"),
                            str(med_dict.get("created_at") or self._now_sp()),
                        ),
                    )

                for prof in professionals:
                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO professionals (id, name, professional_registration, password, created_at)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            str(prof["id"]),
                            prof["name"],
                            prof["professional_registration"],
                            prof.get("password", ""),
                            str(prof.get("created_at") or self._now_sp()),
                        ),
                    )

                for server_pat in patients:
                    pat_id = str(server_pat["id"])
                    cursor.execute("SELECT * FROM patients WHERE id = ?", (pat_id,))
                    local_row = cursor.fetchone()

                    if local_row:
                        local_pat = dict(local_row)
                        winner = self.strategy.resolve(local_pat, server_pat)
                        is_synced = (
                            0
                            if winner == local_pat and local_pat.get("is_synced") == 0
                            else 1
                        )
                    else:
                        winner = server_pat
                        is_synced = 1

                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO patients (id, name, document, created_at, is_synced)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            str(winner["id"]),
                            winner["name"],
                            winner["document"],
                            str(winner.get("created_at") or self._now_sp()),
                            is_synced,
                        ),
                    )

                for server_rec in records:
                    rec_id = str(server_rec["id"])
                    cursor.execute(
                        "SELECT * FROM medical_records WHERE id = ?", (rec_id,)
                    )
                    local_row = cursor.fetchone()

                    if local_row:
                        local_rec = dict(local_row)
                        winner = self.strategy.resolve(local_rec, server_rec)
                        is_synced = (
                            0
                            if winner == local_rec and local_rec.get("is_synced") == 0
                            else 1
                        )
                    else:
                        winner = server_rec
                        is_synced = 1

                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO medical_records 
                        (id, patient_id, blood_type, known_allergies, chronic_conditions, emergency_contact, created_at, is_synced)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            str(winner["id"]),
                            str(winner["patient_id"]),
                            winner.get("blood_type"),
                            winner.get("known_allergies"),
                            winner.get("chronic_conditions"),
                            winner.get("emergency_contact"),
                            str(winner.get("created_at") or self._now_sp()),
                            is_synced,
                        ),
                    )

                for att in attendances:
                    att_id = str(att["id"])

                    cursor.execute(
                        "SELECT is_synced FROM attendances WHERE id = ?", (att_id,)
                    )
                    local_row = cursor.fetchone()
                    if local_row and dict(local_row).get("is_synced") == 0:
                        continue

                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO attendances 
                        (id, medical_record_id, professional_id, patient_id, pressure, heart_rate, consciousness_level, triage_protocol, notes, created_at, synchronized_at, is_synced)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
                        """,
                        (
                            att_id,
                            str(att.get("medical_record_id") or ""),
                            str(att.get("professional_id") or ""),
                            str(att.get("patient_id") or ""),
                            att.get("pressure"),
                            att.get("heart_rate"),
                            att.get("consciousness_level"),
                            att.get("triage_protocol"),
                            att.get("notes"),
                            str(att.get("created_at") or self._now_sp()),
                            str(att.get("synchronized_at") or self._now_sp()),
                        ),
                    )

                    meds_list = att.get("medications") or []
                    if isinstance(meds_list, str):
                        meds_list = json.loads(meds_list)

                    for med in meds_list:
                        med_dict = self._to_dict(med)
                        if not med_dict.get("medication_id"):
                            continue
                        med_row_id = str(med_dict.get("id") or uuid4())
                        cursor.execute(
                            """
                            INSERT OR REPLACE INTO attendance_medications 
                            (id, attendance_id, medication_id, applied_dose, applied_at, is_synced)
                            VALUES (?, ?, ?, ?, ?, 1)
                            """,
                            (
                                med_row_id,
                                att_id,
                                str(med_dict["medication_id"]),
                                med_dict.get("applied_dose"),
                                str(
                                    med_dict.get("application_timestamp")
                                    or med_dict.get("applied_at")
                                    or self._now_sp()
                                ),
                            ),
                        )

                conn.commit()
            return None
        except Exception as e:
            raise ValueError(f"Sync failed: {str(e)}")

    async def push_to_database(self) -> dict:
        """Push local records with is_synced = 0 from SQLite to PostgreSQL database using create/insert operations."""
        try:
            with self.sqlite.get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM patients WHERE is_synced = 0")
                unsynced_patients = [dict(row) for row in cursor.fetchall()]

                cursor.execute("SELECT * FROM medical_records WHERE is_synced = 0")
                unsynced_records = [dict(row) for row in cursor.fetchall()]

                cursor.execute("SELECT * FROM attendances WHERE is_synced = 0")
                unsynced_attendances = [dict(row) for row in cursor.fetchall()]

                attendance_ids = [att["id"] for att in unsynced_attendances]
                unsynced_attendance_medications = []
                if attendance_ids:
                    placeholders = ",".join(["?"] * len(attendance_ids))
                    cursor.execute(
                        f"SELECT * FROM attendance_medications WHERE attendance_id IN ({placeholders})",
                        attendance_ids,
                    )
                    unsynced_attendance_medications = [
                        dict(row) for row in cursor.fetchall()
                    ]

            for pat in unsynced_patients:
                await self.patient_repo.create(
                    id=pat["id"], name=pat["name"], document=pat["document"]
                )

            for rec in unsynced_records:
                await self.medical_record_repo.create(
                    id=rec["id"],
                    patient_id=rec["patient_id"],
                    blood_type=rec["blood_type"],
                    known_allergies=rec["known_allergies"],
                    chronic_conditions=rec["chronic_conditions"],
                    emergency_contact=rec["emergency_contact"],
                )

            for att in unsynced_attendances:
                att_meds = [
                    m
                    for m in unsynced_attendance_medications
                    if m["attendance_id"] == att["id"]
                ]
                att["medications"] = att_meds
                await self.attendance_repo.create(
                    id=att["id"],
                    medical_record_id=att["medical_record_id"],
                    professional_id=att["professional_id"],
                    patient_id=att["patient_id"],
                    pressure=att["pressure"],
                    heart_rate=att["heart_rate"],
                    consciousness_level=att["consciousness_level"],
                    triage_protocol=att["triage_protocol"],
                    notes=att["notes"],
                    medications=att["medications"],
                )

            with self.sqlite.get_connection() as conn:
                cursor = conn.cursor()

                for pat in unsynced_patients:
                    cursor.execute(
                        "UPDATE patients SET is_synced = 1 WHERE id = ?", (pat["id"],)
                    )
                for rec in unsynced_records:
                    cursor.execute(
                        "UPDATE medical_records SET is_synced = 1 WHERE id = ?",
                        (rec["id"],),
                    )
                for att in unsynced_attendances:
                    cursor.execute(
                        "UPDATE attendances SET is_synced = 1 WHERE id = ?",
                        (att["id"],),
                    )
                    for med in unsynced_attendance_medications:
                        if med["attendance_id"] == att["id"]:
                            cursor.execute(
                                "UPDATE attendance_medications SET is_synced = 1 WHERE id = ?",
                                (med["id"],),
                            )

                conn.commit()

            return None
        except Exception as e:
            raise ValueError(f"Push sync failed: {str(e)}")

    async def fetch_offline_data(self):
        return {
            "attendances": await self.attendance_repo.fetch_all(),
            "medical_records": await self.medical_record_repo.fetch_all(),
            "patients": await self.patient_repo.fetch_all(),
            "medications": await self.medication_repo.fetch_all(),
        }
