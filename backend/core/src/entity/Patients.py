class Patients(BaseModel):
    name: str = Field(description="The name of the patient")
    document: str = Field(description="The document of the patient")
    created_at: datetime = Field(default_factory=datetime.now, description="The date and time when the patient was created")