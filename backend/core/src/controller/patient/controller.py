from injector import inject

from src.dtos.patient.read import ReadPatientByIdDTO, ReadPatientResponseDTO
from src.use_cases.patient.create import CreatePatientUseCase
from src.use_cases.patient.fetch import FetchPatientUseCase
from src.dtos.patient.create import CreatePatientDTO, CreatePatientResponseDTO
from src.use_cases.patient.fetch_by_id import FetchPatientByIdUseCase


class PatientController:
    @inject
    def __init__(
        self,
        create_use_case: CreatePatientUseCase,
        fetch_use_case: FetchPatientUseCase,
        fetch_by_id_use_case: FetchPatientByIdUseCase
    ):
        self.create_use_case = create_use_case
        self.fetch_use_case = fetch_use_case
        self.fetch_by_id_use_case = fetch_by_id_use_case
        

    async def create(self, payload: CreatePatientDTO) -> CreatePatientResponseDTO:
        return await self.create_use_case.execute(
            payload=CreatePatientDTO(name=payload.name, document=payload.document)
        )

    async def fetch(self) -> ReadPatientResponseDTO:
        return await self.fetch_use_case.execute()

    async def fetch_by_id(self, patient_id: int) -> ReadPatientResponseDTO:
        return await self.fetch_by_id_use_case.execute(ReadPatientByIdDTO(id=patient_id))