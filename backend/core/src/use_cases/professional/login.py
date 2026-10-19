from fastapi import HTTPException, status
from injector import inject

from src.config.errors.db_exceptions import handle_database_error
from src.services.professional.service import ProfessionalService
from src.dtos.professional.login import LoginRequestDTO, LoginResponseDTO
from utils.jwt import create_access_token


class LoginUseCase:
    @inject
    def __init__(self, professional_service: ProfessionalService):
        self.professional_service = professional_service

    async def execute(self, payload: LoginRequestDTO) -> LoginResponseDTO:
        try:
            user = await self.professional_service.fetch_by_professional_registration(payload.professional_registration)

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Profissional não encontrado ou senha incorreta.",
                )

            token_payload = {
                "sub": str(user.id),
                "name": user.name,
                "professional_registration": user.professional_registration,
            }

            access_token = create_access_token(data=token_payload)

            return LoginResponseDTO(access_token=access_token)

        except Exception as e:
            handle_database_error(e)
