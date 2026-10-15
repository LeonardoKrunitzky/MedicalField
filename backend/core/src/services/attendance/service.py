from typing import List, Optional
from uuid import UUID

from injector import inject

from src.dtos.attendance.create import CreateAttendanceMedicationDTO
from src.domains.attendances.repository import AttendanceRepository
from src.dtos.attendance.read import Attendance


class AttendanceService:
    @inject
    def __init__(self, repository: AttendanceRepository):
        self._repository = repository

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
        return await self._repository.create(
            id=id,
            medical_record_id=medical_record_id,
            professional_id=professional_id,
            patient_id=patient_id,
            pressure=pressure,
            heart_rate=heart_rate,
            consciousness_level=consciousness_level,
            triage_protocol=triage_protocol,
            notes=notes,
            medications=medications,
        )

    async def fetch_all(self) ->list[Attendance]:
        return await self._repository.fetch_all()

    async def fetch_by_patient(self, patient_id: UUID) -> list[Attendance]:
        return await self._repository.fetch_by_patient(patient_id)
