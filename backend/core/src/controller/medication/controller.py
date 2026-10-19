from uuid import UUID

from injector import inject

from src.dtos.medication.create import CreateMedicationDTO
from src.dtos.medication.read import Medication, ReadMedicationByAttendanceResponceDTO, ReadMedicationByIdDTO, ReadMedicationResponseDTO
from src.use_cases.medication.create import CreateMedicationsUseCase
from src.use_cases.medication.fetch_all import FetchAllMedicationUseCase
from src.use_cases.medication.fetch_by_attendance import FetchMedicationByAttendanceUseCase


class MedicationController:
    @inject
    def __init__(
        self,
        fetch_all_use_case: FetchAllMedicationUseCase,
        fetch_use_case: FetchMedicationByAttendanceUseCase,
        create_use_case: CreateMedicationsUseCase
    ):
        self.fetch_all_use_case = fetch_all_use_case
        self.fetch_by_attendance_use_case = fetch_use_case
        self.create_use_case = create_use_case

    async def create(self, payload: CreateMedicationDTO) -> Medication:
        return await self.create_use_case.execute(CreateMedicationDTO(name=payload.name, standard_dosage=payload.standard_dosage))

    async def fetch(self) -> ReadMedicationResponseDTO:
        return await self.fetch_all_use_case.execute()

    async def fetch_by_attendance(self, attendance_id: UUID) -> ReadMedicationByAttendanceResponceDTO:
        return await self.fetch_by_attendance_use_case.execute(ReadMedicationByIdDTO(id=attendance_id))