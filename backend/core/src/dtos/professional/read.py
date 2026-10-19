from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

class Professional(BaseModel):
    id: UUID = Field(description="The unique identifier of the professional")
    name: str = Field(description="The name of the professional")
    professional_registration: str = Field(description="The professional registration number of the professional")
    created_at: datetime = Field(description="The date and time when the professional was created")

class ReadAllProfessionalsResponseDTO(BaseModel):
    items: list[Professional] = Field(description="A list of professional objects")