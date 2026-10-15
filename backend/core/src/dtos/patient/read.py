from uuid import UUID

from pydantic import BaseModel, Field
from datetime import datetime


class ReadPatientDTO(BaseModel):
    id: UUID = Field(description="The unique identifier of the patient")
    name: str = Field(description="The name of the patient")
    document: str = Field(description="The document number of the patient")
    created_at: datetime = Field(description="The date and time when the patient was created")

    class Config:
        from_attributes = True
