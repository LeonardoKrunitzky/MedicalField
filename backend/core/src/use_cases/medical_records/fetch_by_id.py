from injector import inject

from src.dtos.medical_record.read import MedicalRecord, ReadMedicalRecordByIdDTO
from src.services.medical_record.service import MedicalRecordService


class FetchMedicalRecordByIdUseCase:
    @inject
    def __init__(self, medical_record_service: MedicalRecordService):
        self.medical_record_service = medical_record_service

    async def execute(self, payload: ReadMedicalRecordByIdDTO) -> MedicalRecord:
        try:
            medical_record = await self.medical_record_service.fetch_by_id(
                patient_id=payload.id
            )

            if not medical_record:
                return None

            return MedicalRecord(
                id=medical_record.id,
                patient_name=medical_record.patient_name,
                blood_type=medical_record.blood_type,
                known_allergies=medical_record.known_allergies,
                chronic_conditions=medical_record.chronic_conditions,
                emergency_contact=medical_record.emergency_contact,
                created_at=medical_record.created_at,
            )
        except Exception as e:
            raise ValueError(f"Fetch medical record by id failed: {str(e)}")
