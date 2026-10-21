from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CreateMedicalRecordDTO(BaseModel):
    patient_id: UUID = Field(description="The unique identifier of the patient")
    blood_type: str = Field(description="The blood type of the patient")
    known_allergies: str = Field(description="Any known allergies of the patient")
    chronic_conditions: str = Field(description="Any chronic conditions of the patient")
    emergency_contact: str = Field(
        description="The emergency contact information for the patient"
    )
    is_offline: Optional[bool] = Field(default=False, description="Indicates whether the attendance was recorded offline or online")
    professional_id: Optional[UUID] = Field(default=None, description="The unique identifier of the professional associated with the attendance")

class CreateMedicalRecordResponseDTO(BaseModel):
    id: UUID = Field(description="The unique identifier of the medical record")
    patient_id: UUID = Field(description="The unique identifier of the patient")
    blood_type: str = Field(description="The blood type of the patient")
    known_allergies: str = Field(description="The known allergies of the patient")
    chronic_conditions: str = Field(description="The chronic conditions of the patient")
    emergency_contact: str = Field(
        description="The emergency contact information for the patient"
    )
    created_at: datetime = Field(
        description="The date and time when the medical record was created"
    )
