from injector import inject
from src.config.errors.db_exceptions import handle_database_error
from src.dtos.medication.create import CreateMedicationDTO, CreateMedicationResponseDto
from src.services.medication.service import MedicationService
from src.utils.uuid5 import generate_uuid5


class CreateMedicationsUseCase:
    @inject
    def __init__(self, medication_service: MedicationService):
        self.medication_service = medication_service

    async def execute(
        self, payload: CreateMedicationDTO
    ) -> CreateMedicationResponseDto:
        try:
            medication = await self.medication_service.create(
                id=generate_uuid5(payload),
                name=payload.name,
                standard_dosage=payload.standard_dosage,
            )
            return CreateMedicationResponseDto(**medication)
        except Exception as e:
            handle_database_error(e)
