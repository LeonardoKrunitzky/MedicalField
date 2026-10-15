from uuid import UUID

from injector import inject

from src.dtos.medical_record.read import (
    MedicalRecord,
    ReadMedicalRecordByIdDTO,
    ReadMedicalRecordsResponseDTO,
)
from src.use_cases.medical_records.create import CreateMedicalRecordUseCase
from src.use_cases.medical_records.fetch_all import FetchAllMedicalRecordsUseCase
from src.use_cases.medical_records.fetch_by_id import FetchMedicalRecordByIdUseCase
from src.use_cases.medical_records.fetch_by_patient import (
    FetchMedicalRecordByPatientUseCase,
)
from src.dtos.medical_record.create import (
    CreateMedicalRecordDTO,
    CreateMedicalRecordResponseDTO,
)


class MedicalRecordController:
    @inject
    def __init__(
        self,
        create_use_case: CreateMedicalRecordUseCase,
        fetch_all_use_case: FetchAllMedicalRecordsUseCase,
        fetch_by_patient_use_case: FetchMedicalRecordByPatientUseCase,
        fetch_by_id_use_case: FetchMedicalRecordByIdUseCase,
    ):
        self.create_use_case = create_use_case
        self.fetch_all_use_case = fetch_all_use_case
        self.fetch_by_patient_use_case = fetch_by_patient_use_case
        self.fetch_by_id_use_case = fetch_by_id_use_case

    async def create(
        self, request: CreateMedicalRecordDTO
    ) -> CreateMedicalRecordResponseDTO:
        return await self.create_use_case.execute(
            CreateMedicalRecordDTO(
                patient_id=request.patient_id,
                blood_type=request.blood_type,
                known_allergies=request.known_allergies,
                chronic_conditions=request.chronic_conditions,
                emergency_contact=request.emergency_contact,
            )
        )

    async def fetch_all(self) -> ReadMedicalRecordsResponseDTO:
        return await self.fetch_all_use_case.execute()

    async def fetch_by_patient(self, patient_id: UUID) -> MedicalRecord:
        return await self.fetch_by_patient_use_case.execute(
            ReadMedicalRecordByIdDTO(id=patient_id)
        )

    async def fetch_by_id(self, patient_id: UUID) -> MedicalRecord:
        return await self.fetch_by_id_use_case.execute(
            ReadMedicalRecordByIdDTO(id=patient_id)
        )