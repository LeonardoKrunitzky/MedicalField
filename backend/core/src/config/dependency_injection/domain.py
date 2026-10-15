from injector import (Module, provider, singleton)

from src.persistence.repository.professional.professional import ProfessionalRepositoryPostgreSQL
from src.connections.pgsql.connection import PostgreSQLClient
from src.domains.professional.repository import ProfessionalRepository


class DomainModule(Module):
    @provider
    @singleton
    def provide_professional_repository(self, client: PostgreSQLClient) -> ProfessionalRepository:
        return ProfessionalRepositoryPostgreSQL(db=client)