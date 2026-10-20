from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field
from typing import Optional, List

class CreateAttendanceMedicationDTO(BaseModel):
    id: Optional[UUID] = Field(default=None)
    medication_id: UUID = Field(description="The unique identifier of the medication")
    applied_dose: str = Field(description="The dose of the medication that was applied")
    applied_at: datetime = Field(description="The date and time when the medication was applied")

class CreateAttendanceDTO(BaseModel):
    medical_record_id: UUID = Field(description="The unique identifier of the medical record associated with the attendance")
    professional_id: UUID = Field(description="The unique identifier of the professional associated with the attendance")
    patient_id: UUID = Field(description="The unique identifier of the patient associated with the attendance")
    pressure: str = Field(description="The blood pressure reading of the patient during the attendance")
    heart_rate: int = Field(description="The heart rate of the patient during the attendance")
    consciousness_level: int = Field(description="The level of consciousness of the patient during the attendance")
    triage_protocol: str = Field(description="The triage protocol used during the attendance")
    notes: Optional[str]  = Field(description="Any additional notes about the attendance")
    medications: Optional[List[CreateAttendanceMedicationDTO]] = Field(description="A list of medications administered during the attendance")
    is_offline: Optional[bool] = Field(default=False, description="Indicates whether the attendance was recorded offline or online")
    professional_id: Optional[UUID] = Field(default=None, description="The unique identifier of the professional associated with the attendance")


class CreateAttendanceResponseDTO(BaseModel):
    id: UUID = Field(description="The unique identifier of the attendance")
    medical_record_id: UUID = Field(description="The unique identifier of the medical record associated with the attendance")
    professional_id: UUID = Field(description="The unique identifier of the professional associated with the attendance")
    patient_id: UUID = Field(description="The unique identifier of the patient associated with the attendance")
    created_at: datetime = Field(description="The date and time when the attendance was created")
    pressure: str = Field(description="The pressure of the patient")
    heart_rate: int = Field(description="The heart rate of the patient")
    consciousness_level: int = Field(description="The consciousness level of the patient")
    triage_protocol: str = Field(description="The triage protocol used for the patient")
    notes: str = Field(description="The notes associated with the attendance")