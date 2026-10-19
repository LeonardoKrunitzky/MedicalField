from uuid import UUID

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from src.dtos.medical_record.read import MedicalRecord


class Attendance(BaseModel):
    id: UUID = Field(description="The unique identifier of the attendance")
    patient_id: UUID = Field(
        description="The unique identifier of the patient associated with the attendance"
    )
    patient_name: str = Field(
        description="The unique identifier of the patient associated with the attendance"
    )
    medical_record_id: UUID = Field(
        description="The unique identifier of the medical record associated with the attendance"
    )
    professional_id: UUID = Field(
        description="The unique identifier of the professional associated with the attendance"
    )
    professional_name: str = Field(
        description="The unique identifier of the professional associated with the attendance"
    )
    pressure: str = Field(
        description="The blood pressure reading of the patient during the attendance"
    )
    heart_rate: int = Field(
        description="The heart rate of the patient during the attendance"
    )
    consciousness_level: int = Field(
        description="The level of consciousness of the patient during the attendance"
    )
    triage_protocol: str = Field(
        description="The triage protocol used during the attendance"
    )
    notes: Optional[str] = Field(
        description="Any additional notes about the attendance"
    )
    created_at: datetime = Field(
        description="The timestamp when the attendance was created"
    )


class ReadAttendanceResponseDTO(BaseModel):
    items: list[Attendance] = Field(description="A list of medication objects")

class ReadAttendancesByPatientDTO(BaseModel):
    id: UUID = Field(description="The unique identifier of the patient")