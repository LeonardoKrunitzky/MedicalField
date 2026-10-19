from uuid import UUID

from injector import inject

from src.domains.medication.entity import Medication
from src.domains.medication.repository import MedicationRepository
from src.dtos.medication.read import MedicationByAttendance


class MedicationService:
    @inject
    def __init__(self, repository: MedicationRepository):
        self._repository = repository

    async def create(self, id: UUID, name: str, standard_dosage: str) -> Medication:
        return await self._repository.create(
            id=id, name=name, standard_dosage=standard_dosage
        )

    async def fetch_all(self) -> list[Medication]:
        return await self._repository.fetch_all()

    async def fetch_by_attendance(
        self, attendance_id: UUID
    ) -> list[MedicationByAttendance]:
        return await self._repository.fetch_by_attendance(attendance_id=attendance_id)
