from uuid import UUID

from injector import inject

from src.domains.medical_records.repository import MedicalRecordRepository
from src.dtos.medical_record.read import MedicalRecord


class MedicalRecordService:
    @inject
    def __init__(self, repository: MedicalRecordRepository):
        self._repository = repository

    async def create(
        self,
        id: UUID,
        patient_id: UUID,
        blood_type: str,
        known_allergies: str,
        chronic_conditions: str,
        emergency_contact: str,
    ) -> MedicalRecord:
        return await self._repository.create(
            id=id,
            patient_id=patient_id,
            blood_type=blood_type,
            known_allergies=known_allergies,
            chronic_conditions=chronic_conditions,
            emergency_contact=emergency_contact,
        )

    async def fetch_all(self) -> list[MedicalRecord]:
        return await self._repository.fetch_all()

    async def fetch_by_patient(self, patient_id: UUID) -> MedicalRecord:
        return await self._repository.fetch_by_patient(patient_id)

    async def fetch_by_id(self, patient_id: UUID) -> MedicalRecord:
        return await self._repository.fetch_by_id(patient_id)
