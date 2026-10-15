from injector import inject

from src.services.professional.service import ProfessionalServices
from src.dtos.professional.login import LoginRequestDTO, LoginResponseDTO
from utils.jwt import create_access_token


class LoginUseCase:
    @inject
    def __init__(self, professional_service: ProfessionalServices):
        self.professional_service = professional_service

    async def execute(self, payload: LoginRequestDTO) -> LoginResponseDTO:
        try:
            user = await self.professional_service.fetch_by_professional_registration(payload.professional_registration)

            if not user:
                raise ValueError("Invalid username or password")

            token_payload = {
                "sub": str(user.id),
                "name": user.name,
                "professional_registration": user.professional_registration,
            }

            access_token = create_access_token(data=token_payload)

            return LoginResponseDTO(access_token=access_token)

        except Exception as e:
            raise ValueError(f"Login failed: {str(e)}")
