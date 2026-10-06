from injector import inject

from backend.core.src.dtos.authentication.login import LoginRequestDTO, LoginResponseDTO
from backend.core.src.services.authentication import AuthenticationServices
from utils.jwt import create_access_token


class LoginUseCase:
    @inject
    def __init__(self, authentication_service: AuthenticationServices):
        self.authentication_service = authentication_service

    def execute(self, payload: LoginRequestDTO) -> LoginResponseDTO:
        try:
            user = self.authentication_service.login(payload.username, payload.password)

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
