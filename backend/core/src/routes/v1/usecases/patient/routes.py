from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_injector import Injected

from src.controller.patient.controller import PatientController
from src.dtos.patient.create import CreatePatientDTO, CreatePatientResponseDTO
from src.dtos.patient.read import Patient, ReadPatientResponseDTO
from src.config.security.security import verify_token

router = APIRouter(
    prefix="/patient", tags=["Patient"], dependencies=[Depends(verify_token)]
)

@router.post(
    "/",
    summary="Create patient",
    status_code=201,
    response_model=CreatePatientResponseDTO,
    responses={
        409: {"description": "Paciente já cadastrado (documento duplicado)"},
        401: {"description": "Não autorizado"},
        500: {"description": "Erro interno no servidor"},
    },
)
async def create(
    payload: CreatePatientDTO,
    current_user: dict = Depends(verify_token),
    controller: PatientController = Injected(PatientController),
):
    payload.professional_id = UUID(str(current_user.get("sub")))
    return await controller.create(payload)

@router.get(
    "/",
    summary="Fetch patients",
    status_code=200,
    response_model=ReadPatientResponseDTO,
    responses={
        401: {"description": "Não autorizado"},
        500: {"description": "Erro interno no servidor"},
    },
)
async def fetch_all(
    controller: PatientController = Injected(PatientController),
):
    return await controller.fetch_all()

@router.get(
    "/{patient_id}",
    summary="Fetch patient by id",
    status_code=200,
    response_model=Patient,
    responses={
        404: {"description": "Paciente não encontrado"},
        401: {"description": "Não autorizado"},
        500: {"description": "Erro interno no servidor"},
    },
)
async def fetch_by_id(
    patient_id: UUID,
    controller: PatientController = Injected(PatientController),
):
    return await controller.fetch_by_id(patient_id)