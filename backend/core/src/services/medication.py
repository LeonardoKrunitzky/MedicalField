from uuid import UUID

from injector import inject

from backend.core.src.domains.medication.repository import MedicationRepository


class MedicationService:
    @inject
    def __init__(self, repository: MedicationRepository):
        self._repository = repository

    async def fetch_medications(self):
        return await self._repository.fetch_medications()

    async def register_medication(self, id: UUID, name: str, standard_dosage: str):
        return await self.repository.register_medication(
            id=id, name=name, standard_dosage=standard_dosage
        )
