from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_injector import Injected

from src.controller.attendance.controller import AttendanceController
from src.dtos.attendance.create import CreateAttendanceDTO, CreateAttendanceResponseDTO
from src.dtos.attendance.read import ReadAttendanceResponseDTO, Attendance
from src.config.security.security import verify_token

router = APIRouter(
    prefix="/attendance", tags=["Attendance"], dependencies=[Depends(verify_token)]
)

@router.post(
    "/",
    summary="Create a new attendance",
    status_code=201,
    response_model=CreateAttendanceResponseDTO
)
async def create(
    payload: CreateAttendanceDTO,
    controller: AttendanceController = Injected(AttendanceController),
):
    return await controller.create(payload)


@router.get(
    "/",
    summary="Fetch all attendances",
    status_code=200,
    response_model=ReadAttendanceResponseDTO,
)
async def fetch_all_attendances(
    controller: AttendanceController = Injected(AttendanceController),
):
    return await controller.fetch_all()


@router.get(
    "/{patient_id}",
    summary="Fetch attendances by patient",
    status_code=200,
    response_model=Attendance,
)
async def fetch_by_patient(
    patient_id: UUID,
    controller: AttendanceController = Injected(AttendanceController),
):
    return await controller.fetch_by_patient(patient_id)
