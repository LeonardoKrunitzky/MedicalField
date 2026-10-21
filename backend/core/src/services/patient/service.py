from datetime import datetime
from uuid import UUID

from injector import inject

from src.domains.patients.entity import Patient
from src.domains.patients.repository import PatientOfflineRepository, PatientRepository


class PatientService:
    @inject
    def __init__(self, repository: PatientRepository):
        self._repository = repository

    async def create(
        self, id: UUID, name: str, document: str, created_at: datetime
    ) -> Patient:
        return await self._repository.create(
            id=id, name=name, document=document, created_at=created_at
        )

    async def fetch_all(self) -> list[Patient]:
        return await self._repository.fetch_all()

    async def fetch_by_id(self, patient_id: UUID) -> Patient:
        return await self._repository.fetch_by_id(patient_id=patient_id)


class PatientOfflineService:
    @inject
    def __init__(self, repository: PatientOfflineRepository):
        self._repository = repository

    async def save_patient_offline(
        self,
        id: UUID,
        name: str,
        document: str,
        created_at: datetime,
    ) -> Patient:
        return await self._repository.save_patient_offline(
            id=id,
            name=name,
            document=document,
            created_at=created_at,
        )
