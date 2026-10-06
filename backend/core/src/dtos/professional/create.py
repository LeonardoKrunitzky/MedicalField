from uuid import UUID

from pydantic import BaseModel


class CreateProfessionalDTO(BaseModel):
    name: str
    professional_registration: str
    password: str