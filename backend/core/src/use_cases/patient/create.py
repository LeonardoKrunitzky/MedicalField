from injector import inject

from src.utils.uuid5 import generate_uuid5
from src.dtos.patient.create import CreatePatientDTO, CreatePatientResponseDTO
from src.services.patient.service import PatientService


class CreatePatientUseCase:
    @inject
    def __init__(self, patient_service: PatientService):
        self.patient_service = patient_service

    async def execute(self, payload: CreatePatientDTO) -> CreatePatientResponseDTO:
        try:

            patient = await self.patient_service.create(
                id=generate_uuid5(payload), name=payload.name, document=payload.document
            )

            return CreatePatientResponseDTO(**patient)
        except Exception as e:
            raise ValueError(f"Create patient failed: {str(e)}")
