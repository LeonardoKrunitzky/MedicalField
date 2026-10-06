import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class MedicalRecords(BaseModel):
    id: UUID = Field(description="The unique identifier of the medical record")
    patient_id: UUID = Field(description="The unique identifier of the patient")
    blood_type: str = Field(description="The blood type of the patient")
    known_allergies: str = Field(description="The known allergies of the patient")
    chronic_diseases: str = Field(description="The chronic diseases of the patient")
    created_at: datetime = Field(description="The date and time when the medical record was created")