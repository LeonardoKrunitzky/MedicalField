from injector import inject

from src.dtos.attendance.read import Attendance, ReadAttendancesByPatientDTO
from src.services.attendance.service import AttendanceService


class FetchAttendancesByPatientUseCase:
    @inject
    def __init__(self, attendance_service: AttendanceService):
        self.attendance_service = attendance_service

    async def execute(self, patient_id: ReadAttendancesByPatientDTO) -> Attendance:
        try:
            attendance = await self.attendance_service.fetch_by_patient(
                patient_id=patient_id
            )
            if not attendance:
                return None

            return [
                Attendance(
                    id=attendance.id,
                    medical_record_id=attendance.medical_record_id,
                    professional_id=attendance.professional_id,
                    pressure=attendance.pressure,
                    heart_rate=attendance.heart_rate,
                    consciousness_level=attendance.consciousness_level,
                    triage_protocol=attendance.triage_protocol,
                    notes=attendance.notes,
                    created_at=attendance.created_at,
                    synchronized_at=attendance.synchronized_at,
                )
            ]
        except Exception as e:
            raise ValueError(f"Fetch attendances by patient failed: {str(e)}")
