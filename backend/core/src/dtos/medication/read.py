from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

class Medication(BaseModel):
    id: UUID = Field(description="The unique identifier of the medication")
    name: str = Field(description="The name of the medication")
    standard_dosage: str = Field(description="The standard dosage of the medication")
    created_at: datetime = Field(description="The date and time when the medication was created")

class MedicationByAttendance(BaseModel):
    id: UUID = Field(description="The unique identifier of the medication")
    name: str = Field(description="The name of the medication")
    standard_dosage: str = Field(description="The standard dosage of the medication")
    applied_dose: str = Field(description="The dose of the medication that was applied")
    applied_at: datetime = Field(description="The date and time when the medication was applied")

class ReadMedicationResponseDTO(BaseModel):
    items: list[Medication] = Field(description="A list of medication objects")

class ReadMedicationByIdDTO(BaseModel):
    id: UUID = Field(description="The unique identifier of the patient")

class ReadMedicationByAttendanceResponceDTO(BaseModel):
    items: list[MedicationByAttendance] = Field(description="A list of medication objects")