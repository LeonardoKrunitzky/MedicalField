from injector import (Module, provider, singleton)

from src.domains.attendances.repository import AttendanceRepository
from src.domains.medical_records.repository import MedicalRecordRepository
from src.domains.patients.repository import PatientRepository
from src.persistence.pgsql.repository.attendance.repository import AttendanceRepositoryPostgreSQL
from src.persistence.pgsql.repository.medical_record.repository import MedicalRecordRepositoryPostgreSQL
from src.persistence.pgsql.repository.medication.repository import MedicationRepositoryPostgreSQL
from src.domains.medication.repository import MedicationRepository
from src.persistence.pgsql.repository.patient.repository import PatientRepositoryPostgreSQL
from src.persistence.pgsql.repository.professional.repository import ProfessionalRepositoryPostgreSQL
from src.connections.pgsql.connection import PostgreSQLClient
from src.domains.professional.repository import ProfessionalRepository


class DomainModule(Module):
    @provider
    @singleton
    def provide_professional_repository(self, client: PostgreSQLClient) -> ProfessionalRepository:
        return ProfessionalRepositoryPostgreSQL(db=client)

    @provider
    @singleton
    def provide_medication_repository(self, client: PostgreSQLClient) -> MedicationRepository:
        return MedicationRepositoryPostgreSQL(db=client)

    @provider
    @singleton
    def provide_attendance_repository(self, client: PostgreSQLClient) -> AttendanceRepository:
        return AttendanceRepositoryPostgreSQL(db=client)

    @provider
    @singleton
    def provide_medical_record_repository(self, client: PostgreSQLClient) -> MedicalRecordRepository:
        return MedicalRecordRepositoryPostgreSQL(db=client)

    @provider
    @provider
    def provide_patients_repository(self, client: PostgreSQLClient) -> PatientRepository:
        return PatientRepositoryPostgreSQL(db=client)