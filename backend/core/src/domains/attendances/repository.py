from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.dtos.attendance.read import Attendance
from src.dtos.attendance.create import CreateAttendanceMedicationDTO


class AttendanceRepository(ABC):
    @abstractmethod
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
        """
        Create a new attendance, including optional attendance_medications.
        """
        pass

    @abstractmethod
    async def fetch_all(self) -> list[Attendance]:
        """
        Fetch all attendances from the database.
        :return: A list of dictionaries representing the attendances.
        """
        pass

    @abstractmethod
    async def fetch_by_patient(self, patient_id: UUID) -> list[Attendance]:
        """
        Fetch all attendances related to a specific patient.
        """
        pass
