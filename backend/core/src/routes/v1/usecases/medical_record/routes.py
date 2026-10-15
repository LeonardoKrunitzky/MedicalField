from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_injector import Injected

from src.controller.medical_record.controller import MedicalRecordController
from src.dtos.medical_record.create import CreateMedicalRecordDTO, CreateMedicalRecordResponseDTO
from src.dtos.medical_record.read import MedicalRecord, ReadMedicalRecordsResponseDTO
from src.config.security.security import verify_token

router = APIRouter(
    prefix="/medical-record", tags=["Medical Record"], dependencies=[Depends(verify_token)]
)

@router.post(
    "/",
    summary="Create a new medical record",
    status_code=201,
    response_model=CreateMedicalRecordResponseDTO,
    responses={
        404: {"description": "Paciente não encontrado"},
        409: {"description": "Paciente já possui um prontuário cadastrado"},
        401: {"description": "Não autorizado"},
        500: {"description": "Erro interno no servidor"},
    },
)
async def create(
    payload: CreateMedicalRecordDTO,
    controller: MedicalRecordController = Injected(MedicalRecordController),
):
    return await controller.create(payload)

@router.get(
    "/",
    summary="Fetch all medical records",
    status_code=200,
    response_model=ReadMedicalRecordsResponseDTO,
    responses={
        401: {"description": "Não autorizado"},
        500: {"description": "Erro interno no servidor"},
    },
)
async def fetch_all(
    controller: MedicalRecordController = Injected(MedicalRecordController),
):
    return await controller.fetch_all()

@router.get(
    "/patient/{patient_id}",
    summary="Fetch medical record by patient",
    status_code=200,
    response_model=MedicalRecord,
    responses={
        404: {
            "description": "Prontuário não encontrado para o paciente informado"
        },
        401: {"description": "Não autorizado"},
        500: {"description": "Erro interno no servidor"},
    },
)
async def fetch_by_patient(
    patient_id: UUID,
    controller: MedicalRecordController = Injected(MedicalRecordController),
):
    return await controller.fetch_by_patient(patient_id)

@router.get(
    "/record/{medical_record_id}",
    summary="Fetch medical record by id",
    status_code=200,
    response_model=MedicalRecord,
    responses={
        404: {"description": "Prontuário médico não encontrado"},
        401: {"description": "Não autorizado"},
        500: {"description": "Erro interno no servidor"},
    },
)
async def fetch_by_id(
    id: UUID,
    controller: MedicalRecordController = Injected(MedicalRecordController),
):
    return await controller.fetch_by_id(id)