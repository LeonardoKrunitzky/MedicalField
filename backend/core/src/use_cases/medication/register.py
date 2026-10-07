from injector import inject

from src.services.medication import MedicationService
from src.domains.medication.repository import MedicationRepository
from src.dtos.medication.create import CreateMedicationDTO
from utils.uuid5 import generate_uuid5_from_payload


class RegisterMedicationUseCase:

    @inject
    def __init__(self, medication_service: MedicationService):
        self.medication_service = medication_service

    async def execute(self, payload: CreateMedicationDTO):
        try:
            await self.medication_service.register_medication(
                id=generate_uuid5_from_payload(payload=payload),
                name=payload.name,
                standard_dosage=payload.standard_dosage,
            )
        except Exception as e:
            raise ValueError(f"Register medication failed: {str(e)}")
