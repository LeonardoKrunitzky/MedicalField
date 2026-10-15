from fastapi import APIRouter

from src.dtos.professional.create import CreateProfessionalDTO
from backend.core.src.controller.professional.controller import ProfessionalController
from src.dtos.professional.login import LoginRequestDTO, LoginResponseDTO
from fastapi_injector import Injected

router = APIRouter(
    prefix="/professional",
    tags=["professional"],
)


@router.post(
    "/register",
    summary="Register a new user",
    status_code=201,
)
async def register(
    payload: CreateProfessionalDTO,
    controller: ProfessionalController = Injected(ProfessionalController),
):
    await controller.register(payload=payload)


@router.post(
    "/login",
    summary="Authenticate a user and return an access token",
    status_code=200,
    response_model=LoginResponseDTO,
)
async def login(
    payload: LoginRequestDTO,
    controller: ProfessionalController = Injected(ProfessionalController),
) -> LoginResponseDTO:
    """
    Authenticate a user and return an access token.

    - **professional_registration**: The registration number of the user.
    - **password**: The password of the user.
    """
    return await controller.login(payload=payload)
