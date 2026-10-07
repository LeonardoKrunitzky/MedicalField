from fastapi import APIRouter
from fastapi_injector import Injected

from src.controller.medication.controller import MedicationController
from src.dtos.medication.read import ReadMedicationDTO
from src.dtos.medication.create import CreateMedicationDTO

router = APIRouter(prefix="/medication", tags=["professional"])


@router.post(
    "/register_medication",
    summary="Register a new medication",
    status_code=201,
)
async def register_medication(
    payload: CreateMedicationDTO,
    controller: MedicationController = Injected(MedicationController),
):
    await controller.register_medication(payload=payload)


@router.get(
    "/fetch_medications",
    summary="Fetch medications",
    status_code=200,
    response_model=list[ReadMedicationDTO],
)
async def fetch_medications(
    controller: MedicationController = Injected(MedicationController),
):
    return await controller.fetch_medications()
