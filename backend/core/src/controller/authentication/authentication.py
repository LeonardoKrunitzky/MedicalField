from injector import inject

from backend.core.src.dtos.authentication.login import LoginRequestDTO, LoginRequestDTO

from backend.core.src.dtos.authentication.login import LoginResponseDTO
from backend.core.src.use_cases.authentication.login import LoginUseCase


class AuthenticationController:
    @inject
    def __init__(self, login_use_case: LoginUseCase):
        self.login_use_case = login_use_case

    def login(self, payload: LoginRequestDTO) -> LoginResponseDTO:
        access_token = self.login_use_case.execute(
            payload=LoginRequestDTO(
                username=payload.username, password=payload.password
            )
        )
        return LoginResponseDTO(access_token=access_token)
