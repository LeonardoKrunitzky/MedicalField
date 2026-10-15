from injector import inject

from src.use_cases.medication.fetch import FetchMedicationUseCase


class MedicationController:
    @inject
    def __init__(
        self,
        fetch_medication_use_case: FetchMedicationUseCase,
    ):
        self.fetch_medication_use_case = fetch_medication_use_case

    async def fetch_medications(self):
        return await self.fetch_medication_use_case.execute()
