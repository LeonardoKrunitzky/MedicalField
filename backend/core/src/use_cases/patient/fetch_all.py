from injector import inject

from src.dtos.patient.read import ReadPatientResponseDTO
from src.services.patient.service import PatientService

class FetchPatientUseCase:
    @inject
    def __init__(self, patient_service: PatientService):
        self.patient_service = patient_service

    async def execute(self) -> ReadPatientResponseDTO:
        try:
            patients = await self.patient_service.fetch_all()
            return ReadPatientResponseDTO(items=patients)
        except Exception as e:
            raise ValueError(f"Fetch patients failed: {str(e)}")