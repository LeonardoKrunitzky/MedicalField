from datetime import datetime
from zoneinfo import ZoneInfo

from injector import inject

from src.config.errors.db_exceptions import handle_database_error
from src.utils.uuid5 import generate_uuid5
from src.dtos.patient.create import CreatePatientDTO, CreatePatientResponseDTO
from src.services.patient.service import PatientOfflineService, PatientService


class CreatePatientUseCase:
    @inject
    def __init__(
        self,
        patient_service: PatientService,
        patient_offline_service: PatientOfflineService,
    ):
        self.patient_service = patient_service
        self.patient_offline_service = patient_offline_service

    async def execute(self, payload: CreatePatientDTO) -> CreatePatientResponseDTO:
        try:

            patient = await self.patient_service.create(
                id=generate_uuid5(payload),
                name=payload.name,
                document=payload.document,
                created_at=datetime.now(ZoneInfo("America/Sao_Paulo")),
            )

            return CreatePatientResponseDTO(**patient)
        except Exception as e:
            handle_database_error(
                e,
                custom_conflict_msg="Já existe um paciente cadastrado com este documento.",
            )

    async def execute_offline(self, payload: CreatePatientDTO):
        try:
            return await self.patient_offline_service.save_patient_offline(
                id=generate_uuid5(payload),
                name=payload.name,
                document=payload.document,
                created_at=datetime.now(ZoneInfo("America/Sao_Paulo")),
            )
        except Exception as e:
            handle_database_error(e)
