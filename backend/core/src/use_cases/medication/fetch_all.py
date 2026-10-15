from injector import inject

from src.services.medication.service import MedicationService
from src.dtos.medication.read import ReadMedicationResponseDTO


class FetchAllMedicationUseCase:

    @inject
    def __init__(self, medication_service: MedicationService) -> ReadMedicationResponseDTO:
        self.medication_service = medication_service

    async def execute(self):
        try:
            result = await self.medication_service.fetch_all()
            return ReadMedicationResponseDTO(items=result)
        except Exception as e:
            raise ValueError(f"Fetch medications failed: {str(e)}")
