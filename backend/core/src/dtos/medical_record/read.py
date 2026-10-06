from uuid import UUID

from pydantic import BaseModel, Field
from datetime import datetime


class ReadMedicalRecordDTO(BaseModel):
    id: UUID = Field(description="The unique identifier of the medical record")
    patient_id: UUID = Field(
        description="The unique identifier of the patient associated with the medical record"
    )
    blood_type: str = Field(description="The blood type of the patient")
    known_allergies: str = Field(description="Any known allergies of the patient")
    chronic_conditions: str = Field(description="Any chronic conditions of the patient")
    emergency_contact: str = Field(
        description="The emergency contact information for the patient"
    )
    created_at: datetime = Field(
        description="The date and time when the medical record was created"
    )

    class Config:
        from_attributes = True
