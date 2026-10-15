from fastapi import APIRouter, Depends
from fastapi_injector import Injected

from src.controller.medication.controller import MedicationController
from src.dtos.medication.read import ReadMedicationResponseDTO
from src.config.security.security import verify_token

router = APIRouter(
    prefix="/medication", tags=["medication"], dependencies=[Depends(verify_token)]
)

@router.get(
    "/fetch_medications",
    summary="Fetch medications",
    status_code=200,
    response_model=ReadMedicationResponseDTO,
)
async def fetch_medications(
    controller: MedicationController = Injected(MedicationController),
):
    return await controller.fetch_medications()
