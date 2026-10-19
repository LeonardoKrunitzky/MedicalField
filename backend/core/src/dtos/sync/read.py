from pydantic import BaseModel

from src.dtos.attendance.read import ReadAttendanceResponseDTO
from src.dtos.medical_record.read import ReadMedicalRecordsResponseDTO
from src.dtos.medication.read import ReadMedicationResponseDTO
from src.dtos.patient.read import ReadPatientResponseDTO


class OfflineDbResponse(BaseModel):
    attendances: list[ReadAttendanceResponseDTO]
    medical_records: list[ReadMedicalRecordsResponseDTO]
    patients: list[ReadPatientResponseDTO]
    medications: list[ReadMedicationResponseDTO]