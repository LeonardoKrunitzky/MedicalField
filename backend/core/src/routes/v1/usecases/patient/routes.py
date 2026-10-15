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
    response_model=CreatePatientResponseDTO
)
async def create(
    payload: CreatePatientDTO,
    controller: PatientController = Injected(PatientController),
):
    return await controller.create(payload)

@router.get(
    "/",
    summary="Fetch patients",
    status_code=200,
    response_model=ReadPatientResponseDTO,
)
async def fetch(
    controller: PatientController = Injected(PatientController),
):
    return await controller.fetch()

@router.get(
    "/{patient_id}",
    summary="Fetch patient by id",
    status_code=200,
    response_model=Patient,
)
async def fetch_by_id(
    patient_id: UUID,
    controller: PatientController = Injected(PatientController),
):
    return await controller.fetch_by_id(patient_id)