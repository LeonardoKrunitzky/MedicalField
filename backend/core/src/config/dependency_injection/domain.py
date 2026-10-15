from injector import (Module, provider, singleton)

from src.persistence.pgsql.repository.medication.repository import MedicationRepositoryPostgreSQL
from src.domains.medication.repository import MedicationRepository
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