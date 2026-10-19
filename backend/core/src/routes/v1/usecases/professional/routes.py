from fastapi import APIRouter, Depends

from src.config.security.security import verify_token
from src.controller.professional.controller import ProfessionalController
from src.dtos.professional.read import ReadAllProfessionalsResponseDTO
from src.dtos.professional.login import LoginRequestDTO, LoginResponseDTO
from fastapi_injector import Injected

router = APIRouter(
    prefix="/professional",
    tags=["Professional"],
)


@router.post(
    "/login",
    summary="Authenticate a user and return an access token",
    status_code=200,
    response_model=LoginResponseDTO,
    responses={
        401: {"description": "Credenciais inválidas (registro ou senha)"},
        500: {"description": "Erro interno no servidor"},
    },
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


@router.get(
    "/",
    summary="Get all professionals",
    status_code=200,
    response_model=ReadAllProfessionalsResponseDTO,
    responses={
        401: {"description": "Credenciais inválidas (registro ou senha)"},
        500: {"description": "Erro interno no servidor"},
    },
     dependencies=[Depends(verify_token)]
)
async def fetch_all(
    controller: ProfessionalController = Injected(ProfessionalController),
):
    return await controller.fetch_all()
