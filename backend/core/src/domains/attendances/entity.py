from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class Attendances(BaseModel):
    id: UUID = Field(description="The unique identifier of the attendance")
    medical_record_id: UUID = Field(description="The unique identifier of the medical record associated with the attendance")
    professional_id: UUID = Field(description="The unique identifier of the professional associated with the attendance")
    created_at: datetime = Field(description="The date and time when the attendance was created")
    pressure: str = Field(description="The pressure of the patient")
    heart_rate: str = Field(description="The heart rate of the patient")
    consciousness_level: str = Field(description="The consciousness level of the patient")
    triage_protocol: str = Field(description="The triage protocol used for the patient")
    notes: str = Field(description="The notes associated with the attendance")
    synchronized_at: datetime = Field(description="The date and time when the attendance was synchronized with the external system")