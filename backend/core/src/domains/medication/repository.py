from abc import ABC, abstractmethod
from uuid import UUID

from src.domains.medication.entity import Medication
from src.dtos.medication.read import MedicationByAttendance

class MedicationRepository(ABC):
    @abstractmethod
    async def fetch_all(self) -> list[Medication]:
        """
        Fetch all medications.

        :return: A list of medication objects.
        """
        pass
    

    @abstractmethod
    async def fetch_by_attendance(self, attendance_id: UUID) -> list[MedicationByAttendance]:
        """
        Fetch a medication by attendance ID.

        :param attendance_id: The ID of the attendance.
        :return: A medication object.
        """
        pass