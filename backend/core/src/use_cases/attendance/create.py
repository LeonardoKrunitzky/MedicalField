from datetime import datetime
import json
from zoneinfo import ZoneInfo

from injector import inject

from src.config.errors.db_exceptions import handle_database_error
from src.utils.uuid5 import generate_uuid5
from src.dtos.attendance.create import (
    CreateAttendanceDTO,
    CreateAttendanceMedicationDTO,
    CreateAttendanceResponseDTO,
)
from src.services.attendance.service import AttendanceOfflineService, AttendanceService


class CreateAttendanceUseCase:
    @inject
    def __init__(
        self,
        attendance_service: AttendanceService,
        attendance_offline_service: AttendanceOfflineService,
    ):
        self.attendance_service = attendance_service
        self.attendance_offline_service = attendance_offline_service

    async def execute(
        self, payload: CreateAttendanceDTO
    ) -> CreateAttendanceResponseDTO:
        try:
            medications_list = []

            for med in payload.medications or []:
                med_dto = CreateAttendanceMedicationDTO(
                    medication_id=med.medication_id,
                    applied_dose=med.applied_dose,
                    applied_at=med.applied_at,
                )
                med_id = generate_uuid5(med_dto, includes_data=True)

                medications_list.append(
                    {
                        "id": str(med_id),
                        "medication_id": str(med.medication_id),
                        "applied_dose": med.applied_dose,
                        "applied_at": str(med.applied_at),
                    }
                )

            response = await self.attendance_service.create(
                id=generate_uuid5(payload, includes_data=True),
                medical_record_id=payload.medical_record_id,
                professional_id=payload.professional_id,
                patient_id=payload.patient_id,
                pressure=payload.pressure,
                heart_rate=payload.heart_rate,
                consciousness_level=payload.consciousness_level,
                triage_protocol=payload.triage_protocol,
                notes=payload.notes,
                medications=medications_list,
                created_at=datetime.now(ZoneInfo("America/Sao_Paulo")),
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
                notes=response.notes
            )
        except Exception as e:
            handle_database_error(
                e,
                custom_conflict_msg="Este atendimento já foi registrado anteriormente.",
            )

    async def execute_offline(self, payload: CreateAttendanceDTO):
        try:
            medications_list = []
            
            for med in payload.medications or []:
                med_dto = CreateAttendanceMedicationDTO(
                    medication_id=med.medication_id,
                    applied_dose=med.applied_dose,
                    applied_at=med.applied_at,
                )
                med_id = generate_uuid5(med_dto)

                medications_list.append(
                    {
                        "id": str(med_id),
                        "medication_id": str(med.medication_id),
                        "applied_dose": med.applied_dose,
                        "applied_at": str(med.applied_at),
                    }
                )

            response = await self.attendance_offline_service.save_attendance_offline(
                id=generate_uuid5(payload, includes_data=True),
                medical_record_id=payload.medical_record_id,
                professional_id=payload.professional_id,
                patient_id=payload.patient_id,
                pressure=payload.pressure,
                heart_rate=payload.heart_rate,
                consciousness_level=payload.consciousness_level,
                triage_protocol=payload.triage_protocol,
                notes=payload.notes,
                medications=medications_list,
                created_at=datetime.now(ZoneInfo("America/Sao_Paulo")),
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
                notes=response.notes
            )
        except Exception as e:
            handle_database_error(e)