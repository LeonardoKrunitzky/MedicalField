import json
import os
from typing import Any
from uuid import UUID, uuid4
import httpx
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
            # 1. Busca os DTOs
            meds_response = await self.medication_repo.fetch_all()
            pats_response = await self.patient_repo.fetch_all()
            recs_response = await self.medical_record_repo.fetch_all()
            atts_response = await self.attendance_repo.fetch_all()
            profs_response = await self.professional_repo.fetch_all()

            # 2. Extrai a lista de '.items' (se for um DTO) ou usa a lista diretamente
            medications = (
                meds_response.items
                if hasattr(meds_response, "items")
                else meds_response
            )
            patients = (
                pats_response.items
                if hasattr(pats_response, "items")
                else pats_response
            )
            records = (
                recs_response.items
                if hasattr(recs_response, "items")
                else recs_response
            )
            attendances = (
                atts_response.items
                if hasattr(atts_response, "items")
                else atts_response
            )
            professionals = (
                profs_response.items
                if hasattr(profs_response, "items")
                else profs_response
            )

            with self.sqlite.get_connection() as conn:
                cursor = conn.cursor()

                for med in medications:
                    med_dict = self._to_dict(med)
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
                    prof_dict = self._to_dict(prof)
                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO professionals (id, name, professional_registration, password, created_at)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            str(prof_dict["id"]),
                            prof_dict["name"],
                            prof_dict.get("professional_registration"),
                            prof_dict.get("password", ""),
                            str(prof_dict.get("created_at") or self._now_sp()),
                        ),
                    )

                for pat in patients:
                    server_pat = self._to_dict(pat)
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

                for rec in records:
                    server_rec = self._to_dict(rec)
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
                    att_dict = self._to_dict(att)
                    att_id = str(att_dict["id"])

                    cursor.execute(
                        "SELECT is_synced FROM attendances WHERE id = ?", (att_id,)
                    )
                    local_row = cursor.fetchone()
                    if local_row and dict(local_row).get("is_synced") == 0:
                        continue

                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO attendances 
                        (id, medical_record_id, professional_id, patient_id, pressure, heart_rate, consciousness_level, triage_protocol, notes, created_at, is_synced)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
                        """,
                        (
                            att_id,
                            str(att_dict.get("medical_record_id") or ""),
                            str(att_dict.get("professional_id") or ""),
                            str(att_dict.get("patient_id") or ""),
                            att_dict.get("pressure"),
                            att_dict.get("heart_rate"),
                            att_dict.get("consciousness_level"),
                            att_dict.get("triage_protocol"),
                            att_dict.get("notes"),
                            str(att_dict.get("created_at") or self._now_sp()),
                        ),
                    )

                    meds_list = att_dict.get("medications") or []
                    if isinstance(meds_list, str):
                        import json

                        meds_list = json.loads(meds_list)

                    for med in meds_list:
                        med_dict = self._to_dict(med)
                        if not med_dict.get("medication_id"):
                            continue

                        from uuid import uuid4

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
            return {"message": "Sincronização concluída com sucesso"}
        except Exception as e:
            raise ValueError(f"Sync failed: {str(e)}")

    async def push_to_database(self) -> dict:
        synced_counts = {
            "patients": 0,
            "medical_records": 0,
            "attendances": 0,
            "logs": 0,
        }

        patients_list = await self.patient_repo.fetch_all()
        records_list = await self.medical_record_repo.fetch_all()

        server_patients = {str(p["id"]): p for p in patients_list}
        server_records = {str(r["id"]): r for r in records_list}

        with self.sqlite.get_connection() as conn:
            cursor = conn.cursor()

            # A) Sincronizar Pacientes
            cursor.execute("SELECT * FROM patients WHERE is_synced = 0")
            for row in cursor.fetchall():
                local_pat = dict(row)
                pat_id = str(local_pat["id"])

                if pat_id in server_patients:
                    winner = self.strategy.resolve(local_pat, server_patients[pat_id])
                else:
                    winner = local_pat

                if winner == local_pat and pat_id not in server_patients:
                    create_fn = getattr(
                        self.patient_repo,
                        "create",
                        getattr(self.patient_repo, "create_patient", None),
                    )
                    await create_fn(
                        id=UUID(pat_id),
                        name=winner["name"],
                        document=winner["document"],
                    )

                cursor.execute(
                    "UPDATE patients SET is_synced = 1 WHERE id = ?", (pat_id,)
                )
                synced_counts["patients"] += 1

            # B) Sincronizar Prontuários
            cursor.execute("SELECT * FROM medical_records WHERE is_synced = 0")
            for row in cursor.fetchall():
                local_rec = dict(row)
                rec_id = str(local_rec["id"])

                if rec_id in server_records:
                    winner = self.strategy.resolve(local_rec, server_records[rec_id])
                else:
                    winner = local_rec

                if winner == local_rec and rec_id not in server_records:
                    create_rec_fn = getattr(
                        self.medical_record_repo,
                        "create",
                        getattr(
                            self.medical_record_repo, "create_medical_record", None
                        ),
                    )
                    await create_rec_fn(
                        id=UUID(rec_id),
                        patient_id=UUID(str(winner["patient_id"])),
                        blood_type=winner.get("blood_type"),
                        known_allergies=winner.get("known_allergies"),
                        chronic_conditions=winner.get("chronic_conditions"),
                        emergency_contact=winner.get("emergency_contact"),
                    )

                cursor.execute(
                    "UPDATE medical_records SET is_synced = 1 WHERE id = ?", (rec_id,)
                )
                synced_counts["medical_records"] += 1

            # C) Sincronizar Atendimentos lendo direto do JSON
            cursor.execute("SELECT * FROM attendances WHERE is_synced = 0")
            for row in cursor.fetchall():
                att = dict(row)
                att_id = str(att["id"])

                # Faz o parse da coluna medications_json
                raw_meds = (
                    json.loads(att["medications_json"])
                    if att.get("medications_json")
                    else []
                )

                # Monta a lista formatada com UUIDs para o repositório do PostgreSQL
                meds = [
                    {
                        "medication_id": UUID(str(m["medication_id"])),
                        "applied_dose": m.get("applied_dose"),
                        "applied_at": m.get("applied_at"),
                    }
                    for m in raw_meds
                ]

                create_att_fn = getattr(
                    self.attendance_repo,
                    "create",
                    getattr(self.attendance_repo, "create_attendance", None),
                )
                await create_att_fn(
                    id=UUID(att_id),
                    medical_record_id=UUID(str(att["medical_record_id"])),
                    professional_id=UUID(str(att["professional_id"])),
                    patient_id=UUID(str(att["patient_id"])) if att.get("patient_id") else None,
                    pressure=att.get("pressure"),
                    heart_rate=att.get("heart_rate"),
                    consciousness_level=att.get("consciousness_level"),
                    triage_protocol=att.get("triage_protocol"),
                    notes=att.get("notes"),
                    medications=meds,
                )

                # Atualiza apenas a tabela attendances
                cursor.execute(
                    "UPDATE attendances SET is_synced = 1 WHERE id = ?", (att_id,)
                )
                synced_counts["attendances"] += 1

            # D) Sincronizar Logs de Auditoria
            cursor.execute("SELECT * FROM offline_audit_logs WHERE is_synced = 0")
            logs = [dict(r) for r in cursor.fetchall()]
            if logs and self.go_logs_url:
                async with httpx.AsyncClient() as client:
                    for log_item in logs:
                        try:
                            await client.post(
                                self.go_logs_url,
                                json={
                                    "client_ip": log_item.get("client_ip"),
                                    "professional_id": log_item.get("professional_id"),
                                    "http_method": log_item.get("http_method"),
                                    "route": log_item.get("route"),
                                    "status_code": log_item.get("status_code"),
                                    "processing_time_ms": log_item.get("processing_time_ms"),
                                },
                                timeout=3.0,
                            )
                        except Exception as e:
                            print(f"Aviso: falha ao enviar log offline para Go: {e}")

                        cursor.execute(
                            "UPDATE offline_audit_logs SET is_synced = 1 WHERE id = ?",
                            (log_item["id"],),
                        )
                        synced_counts["logs"] += 1

            conn.commit()

        return {
            "message": "Sincronização Outbox (SQLite -> PostgreSQL) concluída com sucesso!",
            "synced": synced_counts,
        }

    async def fetch_offline_data(self) -> dict:
        """Busca todos os dados em cache do SQLite local (Offline)."""
        try:
            with self.sqlite.get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM patients")
                patients = [dict(row) for row in cursor.fetchall()]

                cursor.execute("SELECT * FROM medical_records")
                medical_records = [dict(row) for row in cursor.fetchall()]

                cursor.execute("SELECT * FROM medications")
                medications = [dict(row) for row in cursor.fetchall()]

                cursor.execute("SELECT * FROM attendances")
                attendances = [dict(row) for row in cursor.fetchall()]

            # Retorna envelopado com a chave 'items' para satisfazer o schema do Pydantic
            return {
                "attendances": {"items": attendances},
                "medical_records": {"items": medical_records},
                "patients": {"items": patients},
                "medications": {"items": medications},
            }
        except Exception as e:
            raise ValueError(f"Failed to fetch offline data: {str(e)}")