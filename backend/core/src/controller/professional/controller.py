from injector import inject

from src.dtos.professional.read import ReadAllProfessionalsResponseDTO
from src.dtos.professional.login import LoginRequestDTO, LoginRequestDTO

from src.dtos.professional.login import LoginResponseDTO
from src.use_cases.professional.fetch_all import FetchAllProfessionalsUseCase
from src.use_cases.professional.login import LoginUseCase


class ProfessionalController:
    @inject
    def __init__(
        self, login_use_case: LoginUseCase,
        fetch_all_use_case: FetchAllProfessionalsUseCase
    ):
        self.login_use_case = login_use_case
        self.fetch_all_use_case = fetch_all_use_case

    async def login(self, payload: LoginRequestDTO) -> LoginResponseDTO:
        return await self.login_use_case.execute(
            payload=LoginRequestDTO(
                professional_registration=payload.professional_registration,
                password=payload.password,
            )
        )

    async def fetch_all(self) -> ReadAllProfessionalsResponseDTO:
        return await self.fetch_all_use_case.execute()
