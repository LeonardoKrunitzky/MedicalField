from uuid import UUID

from pydantic import BaseModel, Field
from datetime import datetime


class Patient(BaseModel):
    id: UUID = Field(description="The unique identifier of the patient")
    name: str = Field(description="The name of the patient")
    document: str = Field(description="The document number of the patient")
    created_at: datetime = Field(description="The date and time when the patient was created")

class ReadPatientResponseDTO(BaseModel):
    items: list[Patient] = Field(description="A list of patient objects")

class ReadPatientByIdDTO(BaseModel):
    id: UUID = Field(description="The unique identifier of the patient")
