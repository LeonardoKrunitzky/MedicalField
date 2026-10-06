from fastapi import APIRouter

from backend.core.src.controller.authentication.authentication import AuthenticationController
from backend.core.src.dtos.authentication.login import LoginRequestDTO, LoginResponseDTO
from fastapi_injector import Injected

router = APIRouter(
    prefix="/authentication",
    tags=["Authentication"],
)

@router.post(
    "/login",
    summary="Authenticate a user and return an access token",
    status_code=200,
    response_model=LoginResponseDTO,
)
async def login(
    payload: LoginRequestDTO,
    controller: AuthenticationController = Injected(AuthenticationController)
) -> LoginResponseDTO:
    """
    Authenticate a user and return an access token.

    - **username**: The username of the user.
    - **password**: The password of the user.
    """
    return await controller.login(payload=payload)