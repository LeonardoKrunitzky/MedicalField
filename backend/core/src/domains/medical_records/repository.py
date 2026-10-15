from abc import ABC, abstractmethod
from uuid import UUID

from src.domains.medical_records.entity import MedicalRecord


class MedicalRecordRepository(ABC):
    @abstractmethod
    async def create(
        self,
        id: UUID,
        patient_id: UUID,
        blood_type: str,
        known_allergies: str,
        chronic_conditions: str,
        emergency_contact: str,
    ) -> MedicalRecord:
        pass

    @abstractmethod
    async def fetch_all(self) -> list[MedicalRecord]:
        pass

    @abstractmethod
    async def fetch_by_patient(self, patient_id: UUID) -> MedicalRecord:
        pass

    @abstractmethod
    async def fetch_by_id(self, patient_id: UUID) -> MedicalRecord:
        pass
