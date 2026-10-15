from uuid import UUID

from injector import inject

from src.domains.patients.entity import Patient
from src.domains.patients.repository import PatientRepository


class PatientService:
    @inject
    def __init__(self, repository: PatientRepository):
        self._repository = repository

    async def create(self, id: UUID, name: str, document: str) -> Patient:
        return await self._repository.create(id=id, name=name, document=document)

    async def fetch(self) -> list[Patient]:
        return await self._repository.fetch()

    async def fetch_by_id(self, patient_id: UUID) -> Patient:
        return await self._repository.fetch_by_id(patient_id=patient_id)