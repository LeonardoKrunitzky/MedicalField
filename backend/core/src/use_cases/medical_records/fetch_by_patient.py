from fastapi import HTTPException, status
from injector import inject

from src.config.errors.db_exceptions import handle_database_error
from src.dtos.medical_record.read import MedicalRecord, ReadMedicalRecordByIdDTO
from src.services.medical_record.service import MedicalRecordService


class FetchMedicalRecordByPatientUseCase:
    @inject
    def __init__(self, medical_record_service: MedicalRecordService):
        self.medical_record_service = medical_record_service

    async def execute(self, payload: ReadMedicalRecordByIdDTO) -> MedicalRecord:
        try:
            medical_record = await self.medical_record_service.fetch_by_patient(
                patient_id=payload.id
            )
            
            if not medical_record:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Prontuário não encontrado.",
                )

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
            handle_database_error(e)
