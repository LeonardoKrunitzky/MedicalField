from uuid import UUID

from injector import inject

from src.domains.professional.repository import ProfessionalRepository

class ProfessionalServices:
    @inject
    def __init__(self, repository: ProfessionalRepository):
        self._repository = repository

    async def register(self, id: UUID, name: str, professional_registration: str, password: str):
        return await self._repository.create(id, name, professional_registration, password)

    async def read_by_professional_registration(self, professional_registration: str):
        return await self._repository.read_by_professional_registration(professional_registration)