from injector import inject

from src.config.errors.db_exceptions import handle_database_error
from src.utils.uuid5 import generate_uuid5
from src.dtos.medical_record.create import (
    CreateMedicalRecordDTO,
    CreateMedicalRecordResponseDTO,
)
from src.services.medical_record.service import (
    MedicalRecordOfflineService,
    MedicalRecordService,
)


class CreateMedicalRecordUseCase:
    @inject
    def __init__(
        self,
        medical_record_service: MedicalRecordService,
        medical_record_offline_service: MedicalRecordOfflineService,
    ):
        self.medical_record_service = medical_record_service
        self.medical_record_offline_service = medical_record_offline_service

    async def execute(
        self, payload: CreateMedicalRecordDTO
    ) -> CreateMedicalRecordResponseDTO:
        try:
            medical_record = await self.medical_record_service.create(
                id=generate_uuid5(payload),
                patient_id=payload.patient_id,
                blood_type=payload.blood_type,
                known_allergies=payload.known_allergies,
                chronic_conditions=payload.chronic_conditions,
                emergency_contact=payload.emergency_contact,
            )
            return CreateMedicalRecordResponseDTO(**medical_record)
        except Exception as e:
            handle_database_error(
                e,
                custom_conflict_msg="Este paciente já possui um prontuário médico cadastrado.",
            )

    async def execute_offline(
        self, payload: CreateMedicalRecordDTO
    ) -> CreateMedicalRecordResponseDTO:
        try:
            medical_record = (
                await self.medical_record_offline_service.save_medical_record_offline(
                    id=generate_uuid5(payload),
                    patient_id=payload.patient_id,
                    blood_type=payload.blood_type,
                    known_allergies=payload.known_allergies,
                    chronic_conditions=payload.chronic_conditions,
                    emergency_contact=payload.emergency_contact,
                    professional_id=payload.professional_id
                )
            )
            return CreateMedicalRecordResponseDTO(**medical_record)
        except Exception as e:
            handle_database_error(
                e,
                custom_conflict_msg="Este paciente já possui um prontuário médico cadastrado.",
            )
