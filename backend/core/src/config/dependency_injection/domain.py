from injector import Module, provider, singleton

from src.connections.sqlite.connection import SQLiteClient
from src.domains.attendances.repository import (
    AttendanceOfflineRepository,
    AttendanceRepository,
)
from src.domains.medical_records.repository import (
    MedicalRecordOfflineRepository,
    MedicalRecordRepository,
)
from src.domains.patients.repository import PatientOfflineRepository, PatientRepository
from src.domains.sync.repository import SyncRepository
from src.persistence.pgsql.repository.attendance.repository import (
    AttendanceRepositoryPostgreSQL,
)
from src.persistence.pgsql.repository.medical_record.repository import (
    MedicalRecordRepositoryPostgreSQL,
)
from src.persistence.pgsql.repository.medication.repository import (
    MedicationRepositoryPostgreSQL,
)
from src.domains.medication.repository import MedicationRepository
from src.persistence.pgsql.repository.patient.repository import (
    PatientRepositoryPostgreSQL,
)
from src.persistence.pgsql.repository.professional.repository import (
    ProfessionalRepositoryPostgreSQL,
)
from src.connections.pgsql.connection import PostgreSQLClient
from src.domains.professional.repository import ProfessionalRepository
from src.persistence.sqlite.repository.attendance.repository import (
    AttendanceRepositorySQLite,
)
from src.persistence.sqlite.repository.medical_record.repository import (
    MedicalRecordRepositorySQLite,
)
from src.persistence.sqlite.repository.patient.repository import PatientRepositorySQLite
from src.persistence.sqlite.repository.sync.repository import SyncRepositorySQLite


class DomainModule(Module):
    @provider
    @singleton
    def provide_professional_repository(
        self, client: PostgreSQLClient
    ) -> ProfessionalRepository:
        return ProfessionalRepositoryPostgreSQL(db=client)

    @provider
    @singleton
    def provide_medication_repository(
        self, client: PostgreSQLClient
    ) -> MedicationRepository:
        return MedicationRepositoryPostgreSQL(db=client)

    @provider
    @singleton
    def provide_attendance_repository(
        self, client: PostgreSQLClient
    ) -> AttendanceRepository:
        return AttendanceRepositoryPostgreSQL(db=client)

    @provider
    @singleton
    def provide_attendance_offline_repository(
        self, client: SQLiteClient
    ) -> AttendanceOfflineRepository:
        return AttendanceRepositorySQLite(db=client)

    @provider
    @singleton
    def provide_medical_record_repository(
        self, client: PostgreSQLClient
    ) -> MedicalRecordRepository:
        return MedicalRecordRepositoryPostgreSQL(db=client)

    @provider
    @singleton
    def provide_medical_record_offline_repository(
        self, client: SQLiteClient
    ) -> MedicalRecordOfflineRepository:
        return MedicalRecordRepositorySQLite(db=client)

    @provider
    @provider
    def provide_patients_repository(
        self, client: PostgreSQLClient
    ) -> PatientRepository:
        return PatientRepositoryPostgreSQL(db=client)

    @provider
    @singleton
    def provide_patients_offline_repository(
        self, client: SQLiteClient
    ) -> PatientOfflineRepository:
        return PatientRepositorySQLite(db=client)

    @provider
    @singleton
    def provide_sync_client(
        self, sqlite_client: SQLiteClient, pg_client: PostgreSQLClient
    ) -> SyncRepository:
        return SyncRepositorySQLite(
            db=sqlite_client,
            patient_repo=self.provide_patients_repository(pg_client),
            medical_record_repo=self.provide_medical_record_repository(pg_client),
            attendance_repo=self.provide_attendance_repository(pg_client),
            medication_repo=self.provide_medication_repository(pg_client),
            professional_repo=self.provide_professional_repository(pg_client),
        )
