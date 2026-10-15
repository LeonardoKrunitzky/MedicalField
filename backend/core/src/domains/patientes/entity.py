from datetime import datetime
from uuid import UUID, uuid5
from pydantic import BaseModel, Field

class Patients(BaseModel):
    id: UUID = Field(description="The unique identifier of the patient")
    name: str = Field(description="The name of the patient")
    document: str = Field(description="The document of the patient")
    created_at: datetime = Field(description="The date and time when the patient was created")