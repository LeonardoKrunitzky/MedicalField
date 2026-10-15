from injector import inject

from src.config.errors.db_exceptions import handle_database_error
from src.utils.uuid5 import generate_uuid5
from src.dtos.medical_record.create import CreateMedicalRecordDTO, CreateMedicalRecordResponseDTO
from src.services.medical_record.service import MedicalRecordService

class CreateMedicalRecordUseCase:
    @inject
    def __init__(self, medical_record_service: MedicalRecordService):
        self.medical_record_service = medical_record_service

    async def execute(self, payload: CreateMedicalRecordDTO) -> CreateMedicalRecordResponseDTO:
        try:
            medical_record = await self.medical_record_service.create(
                id=generate_uuid5(payload),
                patient_id=payload.patient_id,
                blood_type=payload.blood_type,
                known_allergies=payload.known_allergies,
                chronic_conditions=payload.chronic_conditions,
                emergency_contact=payload.emergency_contact
            )
            return CreateMedicalRecordResponseDTO(**medical_record)
        except Exception as e:
            handle_database_error(
                e, custom_conflict_msg="Este paciente já possui um prontuário médico cadastrado."
            )