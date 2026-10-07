from injector import inject

from src.services.medication import MedicationService


class FetchMedicationUseCase:

    @inject
    def __init__(self, medication_service: MedicationService):
        self.medication_service = medication_service

    async def execute(self):
        try:
            return await self.medication_service.fetch_medications()
        except Exception as e:
            raise ValueError(f"Fetch medications failed: {str(e)}")
