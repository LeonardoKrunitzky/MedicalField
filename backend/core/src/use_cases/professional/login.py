from injector import inject

from utils.bcrypt import verify_password
from src.dtos.professional.login import LoginRequestDTO, LoginResponseDTO
from src.services.professional import ProfessionalServices
from utils.jwt import create_access_token


class LoginUseCase:
    @inject
    def __init__(self, professional_service: ProfessionalServices):
        self.professional_service = professional_service

    async def execute(self, payload: LoginRequestDTO) -> LoginResponseDTO:
        try:
            user = await self.professional_service.read_by_professional_registration(payload.professional_registration)

            if not user or not verify_password(payload.password, user.password):
                raise ValueError("Invalid username or password")

            token_payload = {
                "sub": str(user.id),
                "name": user.name,
                "professional_registration": user.professional_registration,
            }

            response = create_access_token(data=token_payload)

            return response

        except Exception as e:
            raise ValueError(f"Login failed: {str(e)}")
