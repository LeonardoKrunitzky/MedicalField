from fastapi import HTTPException, status
from injector import inject

from src.config.errors.db_exceptions import handle_database_error
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
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Medicamento não encontrado.",
                )
            print(medications)
            return ReadMedicationByAttendanceResponceDTO(items=medications)
        except Exception as e:
            handle_database_error(e)
