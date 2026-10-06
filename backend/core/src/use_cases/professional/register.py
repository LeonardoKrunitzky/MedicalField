from injector import inject

from utils.bcrypt import hash_password
from utils.uuid5 import generate_uuid5_from_payload
from src.dtos.professional.login import LoginRequestDTO, LoginResponseDTO
from src.services.professional import ProfessionalServices


class RegisterUseCase:
    @inject
    def __init__(self, professional_service: ProfessionalServices):
        self.professional_service = professional_service

    async def execute(self, payload: LoginRequestDTO) -> LoginResponseDTO:
        try:
            id = generate_uuid5_from_payload(payload=payload)
            await self.professional_service.register(
                id=id,
                name=payload.name,
                professional_registration=payload.professional_registration,
                password=hash_password(payload.password),
            )

        except Exception as e:
            raise ValueError(f"Register failed: {str(e)}")
