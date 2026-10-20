from pydantic import BaseModel

class OfflineDbResponse(BaseModel):
    attendances: list[dict]
    medical_records: list[dict]
    patients: list[dict]
    medications: list[dict]