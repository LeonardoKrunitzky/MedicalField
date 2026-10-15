from injector import inject

from src.dtos.medication.read import (
    ReadMedicationByAttendanceResponceDTO,
    ReadMedicationByIdDTO,
)
from src.services.medication.service import MedicationService


class FetchMedicationByAttendanceUseCase:
    @inject
    def __init__(self, medication_service: MedicationService):
        self.medication_service = medication_service

    async def execute(
        self, payload: ReadMedicationByIdDTO
    ) -> ReadMedicationByAttendanceResponceDTO:
        try:
            medications = await self.medication_service.fetch_by_attendance(
                attendance_id=payload.id
            )

            if not medications:
                return None

            return ReadMedicationByAttendanceResponceDTO(items=medications)
        except Exception as e:
            raise ValueError(f"Fetch medication by attendance failed: {str(e)}")
