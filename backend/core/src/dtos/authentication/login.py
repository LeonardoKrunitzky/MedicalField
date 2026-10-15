from pydantic import BaseModel, Field

class LoginRequestDTO(BaseModel):
    professional_registration: str = Field(description="The professional registration number of the user")
    password: str = Field(description="The password of the user")

class LoginResponseDTO(BaseModel):
    access_token: str = Field(description="The access token")