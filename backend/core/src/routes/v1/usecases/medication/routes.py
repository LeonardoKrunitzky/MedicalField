from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_injector import Injected

from src.controller.medication.controller import MedicationController
from src.dtos.medication.read import (
    ReadMedicationByAttendanceResponceDTO,
    ReadMedicationResponseDTO,
)
from src.config.security.security import verify_token

router = APIRouter(
    prefix="/medication", tags=["Medication"], dependencies=[Depends(verify_token)]
)


@router.get(
    "/",
    summary="Fetch medications",
    status_code=200,
    response_model=ReadMedicationResponseDTO,
    responses={
        401: {"description": "Não autorizado"},
        500: {"description": "Erro interno no servidor"},
    },
)
async def fetch(
    controller: MedicationController = Injected(MedicationController),
):
    return await controller.fetch()


@router.get(
    "/{atttendence_id}",
    summary="Fetch medication by id",
    status_code=200,
    response_model=ReadMedicationByAttendanceResponceDTO,
    responses={
        404: {"description": "Atendimento não encontrado ou sem medicações aplicadas"},
        401: {"description": "Não autorizado"},
        500: {"description": "Erro interno no servidor"},
    },
)
async def fetch_by_attendance(
    attendance_id: UUID,
    controller: MedicationController = Injected(MedicationController),
):
    return await controller.fetch_by_attendance(attendance_id)
