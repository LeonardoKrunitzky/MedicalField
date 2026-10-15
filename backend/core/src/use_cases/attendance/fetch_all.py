from injector import inject

from src.dtos.attendance.read import ReadAttendanceResponseDTO
from src.services.attendance.service import AttendanceService

class FetchAllAttendancesUseCase:
    @inject
    def __init__(self, attendance_service: AttendanceService):
        self.attendance_service = attendance_service

    async def execute(self) -> ReadAttendanceResponseDTO:
        try:
            attendances = await self.attendance_service.fetch_all()
            return ReadAttendanceResponseDTO(items=attendances)
        except Exception as e:
            raise ValueError(f"Fetch all attendances failed: {str(e)}")