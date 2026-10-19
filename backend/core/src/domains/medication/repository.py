from abc import ABC, abstractmethod
from uuid import UUID

from src.domains.medication.entity import Medication
from src.dtos.medication.read import MedicationByAttendance

class MedicationRepository(ABC):

    @abstractmethod
    async def create(self, id: UUID, name: str, standard_dosage: str) -> Medication:
        pass

    @abstractmethod
    async def fetch_all(self) -> list[Medication]:
        pass
    

    @abstractmethod
    async def fetch_by_attendance(self, attendance_id: UUID) -> list[MedicationByAttendance]:
        pass