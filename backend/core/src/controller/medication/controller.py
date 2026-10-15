from uuid import UUID

from injector import inject

from src.dtos.medication.read import ReadMedicationByIdDTO, ReadMedicationResponseDTO
from src.use_cases.medication.fetch_all import FetchAllMedicationUseCase
from src.use_cases.medication.fetch_by_attendance import FetchMedicationByAttendanceUseCase


class MedicationController:
    @inject
    def __init__(
        self,
        fetch_all_use_case: FetchAllMedicationUseCase,
        fetch_use_case: FetchMedicationByAttendanceUseCase
    ):
        self.fetch_all_use_case = fetch_all_use_case
        self.fetch_by_attendance_use_case = fetch_use_case

    async def fetch(self) -> ReadMedicationResponseDTO:
        return await self.fetch_all_use_case.execute()

    async def fetch_by_attendance(self, attendance_id: UUID) -> ReadMedicationResponseDTO:
        return await self.fetch_by_attendance_use_case.execute(ReadMedicationByIdDTO(id=attendance_id))