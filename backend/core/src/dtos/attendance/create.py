from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field
from typing import Optional, List

class CreateAttendanceMedicationDTO(BaseModel):
    medication_id: UUID = Field(description="The unique identifier of the medication")
    applied_dose: str = Field(description="The dose of the medication that was applied")

class CreateAttendanceDTO(BaseModel):
    id: UUID = Field(description="The unique identifier of the attendance")
    medical_record_id: UUID = Field(description="The unique identifier of the medical record associated with the attendance")
    professional_id: UUID = Field(description="The unique identifier of the professional associated with the attendance")
    pressure: str = Field(description="The blood pressure reading of the patient during the attendance")
    heart_rate: int = Field(description="The heart rate of the patient during the attendance")
    consciousness_level: int = Field(description="The level of consciousness of the patient during the attendance")
    triage_protocol: str = Field(description="The triage protocol used during the attendance")
    notes: Optional[str]  = Field(description="Any additional notes about the attendance")
    medications: Optional[List[CreateAttendanceMedicationDTO]] = Field(description="A list of medications administered during the attendance") 

class CreateAttendanceResponseDTO(BaseModel):
    id: UUID = Field(description="The unique identifier of the attendance")
    medical_record_id: UUID = Field(description="The unique identifier of the medical record associated with the attendance")
    professional_id: UUID = Field(description="The unique identifier of the professional associated with the attendance")
    pressure: str = Field(description="The blood pressure reading of the patient during the attendance")
    heart_rate: int = Field(description="The heart rate of the patient during the attendance")
    consciousness_level: int = Field(description="The level of consciousness of the patient during the attendance")
    triage_protocol: str = Field(description="The triage protocol used during the attendance")
    notes: Optional[str] = Field(description="Any additional notes about the attendance")
    created_at: datetime = Field(description="The timestamp when the attendance was created")
    synchronized_at: Optional[datetime] = Field(description="The timestamp when the attendance was last synchronized")

    class Config:
        from_attributes = True