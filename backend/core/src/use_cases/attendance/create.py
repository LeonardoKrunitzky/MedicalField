import json

from injector import inject

from src.utils.uuid5 import generate_uuid5
from src.dtos.attendance.create import CreateAttendanceDTO, CreateAttendanceMedicationDTO, CreateAttendanceResponseDTO
from src.services.attendance.service import AttendanceService


class CreateAttendanceUseCase:
    @inject
    def __init__(self, attendance_service: AttendanceService):
        self.attendance_service = attendance_service

    async def execute(
        self, request: CreateAttendanceDTO
    ) -> CreateAttendanceResponseDTO:
        try:
            medications_list = []
            
            for med in request.medications:
                med_dto = CreateAttendanceMedicationDTO(
                    medication_id=med.medication_id,
                    applied_dose=med.applied_dose,
                    applied_at=med.applied_at
                )
                med_id = generate_uuid5(med_dto)
                
                medications_list.append({
                    "id": str(med_id),
                    "medication_id": str(med.medication_id),
                    "applied_dose": med.applied_dose,
                    "applied_at": str(med.applied_at)
                })

            response = await self.attendance_service.create(
                id=generate_uuid5(request),
                medical_record_id=request.medical_record_id,
                professional_id=request.professional_id,
                patient_id=request.patient_id,
                pressure=request.pressure,
                heart_rate=request.heart_rate,
                consciousness_level=request.consciousness_level,
                triage_protocol=request.triage_protocol,
                notes=request.notes,
                medications=json.dumps(medications_list)
            )

            return CreateAttendanceResponseDTO(
                id=response.id,
                medical_record_id=response.medical_record_id,
                professional_id=response.professional_id,
                patient_id=response.patient_id,
                created_at=response.created_at,
                pressure=response.pressure,
                heart_rate=response.heart_rate,
                consciousness_level=response.consciousness_level,
                triage_protocol=response.triage_protocol,
                notes=response.notes,
                synchronized_at=response.synchronized_at,
            )
        except Exception as e:
            raise ValueError(f"Create attendance failed: {str(e)}")
