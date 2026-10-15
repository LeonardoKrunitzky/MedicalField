from injector import inject

from src.dtos.professional.login import LoginRequestDTO, LoginRequestDTO

from src.dtos.professional.login import LoginResponseDTO
from src.use_cases.professional.login import LoginUseCase


class ProfessionalController:
    @inject
    def __init__(
        self, login_use_case: LoginUseCase
    ):
        self.login_use_case = login_use_case

    async def login(self, payload: LoginRequestDTO) -> LoginResponseDTO:
        return await self.login_use_case.execute(
            payload=LoginRequestDTO(
                professional_registration=payload.professional_registration,
                password=payload.password,
            )
        )
