from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CreatePatientDTO(BaseModel):
    name: str = Field(description="The name of the patient")
    document: str = Field(description="The document number of the patient")
    is_offline: Optional[bool] = Field(default=False, description="Indicates whether the attendance was recorded offline or online")
    professional_id: Optional[UUID] = Field(default=None, description="The unique identifier of the professional associated with the attendance")


class CreatePatientResponseDTO(BaseModel):
    id: UUID = Field(description="The unique identifier of the patient")
    name: str = Field(description="The name of the patient")
    document: str = Field(description="The document of the patient")
    created_at: datetime = Field(description="The date and time when the patient was created")