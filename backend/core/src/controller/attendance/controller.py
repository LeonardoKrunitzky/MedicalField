from uuid import UUID

from injector import inject

from src.dtos.attendance.read import Attendance, ReadAttendanceResponseDTO, ReadAttendancesByPatientDTO
from src.use_cases.attendance.create import CreateAttendanceUseCase
from src.use_cases.attendance.fetch_all import FetchAllAttendancesUseCase
from src.use_cases.attendance.fetch_by_patient import FetchAttendancesByPatientUseCase
from src.dtos.attendance.create import (
    CreateAttendanceDTO,
    CreateAttendanceMedicationDTO,
    CreateAttendanceResponseDTO,
)


class AttendanceController:
    @inject
    def __init__(
        self,
        create_use_case: CreateAttendanceUseCase,
        fetch_all_use_case: FetchAllAttendancesUseCase,
        fetch_by_patient_use_case: FetchAttendancesByPatientUseCase,
    ):
        self.create_use_case = create_use_case
        self.fetch_all_use_case = fetch_all_use_case
        self.fetch_by_patient_use_case = fetch_by_patient_use_case

    async def create(self, request: CreateAttendanceDTO) -> CreateAttendanceResponseDTO:
        return await self.create_use_case.execute(request)

    async def fetch_all(self) -> ReadAttendanceResponseDTO:
        return await self.fetch_all_use_case.execute()

    async def fetch_by_patient(self, patient_id: UUID) -> Attendance:
        return await self.fetch_by_patient_use_case.execute(
            ReadAttendancesByPatientDTO(patient_id=patient_id)
        )
