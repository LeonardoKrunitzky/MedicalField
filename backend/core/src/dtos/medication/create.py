from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CreateMedicationDTO(BaseModel):
    name: str = Field(description="The name of the medication")
    standard_dosage: str = Field(description="The standard dosage of the medication")
    professional_id: Optional[UUID] = Field(default=None, description="The unique identifier of the professional associated with the medication")

class CreateMedicationResponseDto(BaseModel):
    id: UUID = Field(description="The unique identifier of the medication")
    name: str = Field(description="The name of the medication")
    standard_dosage: str = Field(description="The standard dosage of the medication")
    created_at: datetime = Field(description="The date and time when the medication was created")