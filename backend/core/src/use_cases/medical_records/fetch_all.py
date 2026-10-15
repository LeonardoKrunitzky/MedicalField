from injector import inject

from src.dtos.medical_record.read import ReadMedicalRecordsResponseDTO
from src.services.medical_record.service import MedicalRecordService

class FetchAllMedicalRecordsUseCase:
    @inject
    def __init__(self, medical_record_service: MedicalRecordService):
        self.medical_record_service = medical_record_service

    async def execute(self):
        try:
            medical_records = await self.medical_record_service.fetch_all()
            return ReadMedicalRecordsResponseDTO(items=medical_records)
        except Exception as e:
            raise ValueError(f"Fetch all medical records failed: {str(e)}")