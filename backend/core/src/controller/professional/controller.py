from injector import inject

from src.use_cases.professional.register import RegisterUseCase
from src.dtos.professional.create import CreateProfessionalDTO
from src.dtos.professional.login import LoginRequestDTO, LoginRequestDTO

from src.dtos.professional.login import LoginResponseDTO
from src.use_cases.professional.login import LoginUseCase


class ProfessionalController:
    @inject
    def __init__(
        self, register_use_case: RegisterUseCase, login_use_case: LoginUseCase
    ):
        self.register_use_case = register_use_case
        self.login_use_case = login_use_case

    async def register(self, payload: CreateProfessionalDTO):
        await self.register_use_case.execute(
            payload=CreateProfessionalDTO(
                name=payload.name,
                professional_registration=payload.professional_registration,
                password=payload.password,
            )
        )

    async def login(self, payload: LoginRequestDTO) -> LoginResponseDTO:
        access_token = await self.login_use_case.execute(
            payload=LoginRequestDTO(
                professional_registration=payload.professional_registration,
                password=payload.password,
            )
        )
        return LoginResponseDTO(access_token=access_token)
