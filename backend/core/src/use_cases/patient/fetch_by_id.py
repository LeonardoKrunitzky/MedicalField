from injector import inject

from src.dtos.patient.read import ReadPatientByIdDTO, Patient
from src.services.patient.service import PatientService


class FetchPatientByIdUseCase:
    @inject
    def __init__(self, patient_service: PatientService):
        self.patient_service = patient_service

    async def execute(self, payload: ReadPatientByIdDTO) -> Patient:
        try:
            patient = await self.patient_service.fetch_by_id(patient_id=payload.id)

            if not patient:
                return None

            return Patient(
                id=patient.id,
                name=patient.name,
                document=patient.document,
                created_at=patient.created_at,
            )
        except Exception as e:
            raise ValueError(f"Fetch Patient by id failed: {str(e)}")
