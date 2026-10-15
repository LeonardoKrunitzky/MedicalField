from injector import (Module, provider, singleton)

from backend.core.src.domains.medication.repository import MedicationRepository
from backend.core.src.persistence.repository.professional.repository import ProfessionalRepositoryPostgreSQL
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