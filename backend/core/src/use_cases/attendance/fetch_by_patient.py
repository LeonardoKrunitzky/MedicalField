from fastapi import HTTPException, status
from injector import inject

from src.config.errors.db_exceptions import handle_database_error
from src.dtos.attendance.read import (
    Attendance,
    ReadAttendanceResponseDTO,
    ReadAttendancesByPatientDTO,
)
from src.services.attendance.service import AttendanceService


class FetchAttendancesByPatientUseCase:
    @inject
    def __init__(self, attendance_service: AttendanceService):
        self.attendance_service = attendance_service

    async def execute(
        self, payload: ReadAttendancesByPatientDTO
    ) -> ReadAttendanceResponseDTO:
        try:
            attendances = await self.attendance_service.fetch_by_patient(
                patient_id=payload.id
            )

            if not attendances:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Atendimento não encontrado.",
                )

            return ReadAttendanceResponseDTO(items=attendances)
        except Exception as e:
            handle_database_error(e)