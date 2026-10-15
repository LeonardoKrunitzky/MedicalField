from injector import inject

from src.use_cases.medication.fetch import FetchMedicationUseCase
from src.use_cases.medication.register import RegisterMedicationUseCase
from src.dtos.medication.create import CreateMedicationDTO
from src.dtos.medication.read import ReadMedicationDTO


class MedicationController:
    @inject
    def __init__(
        self,
        register_medication_use_case: RegisterMedicationUseCase,
        fetch_medication_use_case: FetchMedicationUseCase,
    ):
        self.register_medication_use_case = register_medication_use_case
        self.fetch_medication_use_case = fetch_medication_use_case

    async def register_medication(self, payload: CreateMedicationDTO):
        await self.register_medication_use_case.execute(
            payload=CreateMedicationDTO(
                name=payload.name, standard_dosage=payload.standard_dosage
            )
        )

    async def fetch_medications(self):
        result = await self.fetch_medication_use_case.execute()
        return ReadMedicationDTO(result)
