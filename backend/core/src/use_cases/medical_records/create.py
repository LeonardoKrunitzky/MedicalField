from injector import inject

from src.utils.uuid5 import generate_uuid5
from src.dtos.medical_record.create import CreateMedicalRecordDTO, CreateMedicalRecordResponseDTO
from src.services.medical_record.service import MedicalRecordService

class CreateMedicalRecordUseCase:
    @inject
    def __init__(self, medical_record_service: MedicalRecordService):
        self.medical_record_service = medical_record_service

    async def execute(self, request: CreateMedicalRecordDTO) -> CreateMedicalRecordResponseDTO:
        try:
            medical_record = await self.medical_record_service.create(
                id=generate_uuid5(request),
                patient_id=request.patient_id,
                blood_type=request.blood_type,
                known_allergies=request.known_allergies,
                chronic_conditions=request.chronic_conditions,
                emergency_contact=request.emergency_contact
            )
            return CreateMedicalRecordResponseDTO(**medical_record)
        except Exception as e:
            raise ValueError(f"Create medical record failed: {str(e)}")