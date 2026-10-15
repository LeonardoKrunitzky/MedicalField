from injector import inject

from src.dtos.medication.read import ReadMedicationResponseDTO
from src.services.medication import MedicationService


class FetchMedicationUseCase:

    @inject
    def __init__(self, medication_service: MedicationService):
        self.medication_service = medication_service

    async def execute(self):
        try:
            result = await self.medication_service.fetch_medications()
            return ReadMedicationResponseDTO(items=result)
        except Exception as e:
            raise ValueError(f"Fetch medications failed: {str(e)}")
