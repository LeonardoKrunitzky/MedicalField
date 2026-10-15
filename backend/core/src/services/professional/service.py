from uuid import UUID

from injector import inject

from src.domains.professional.entity import Professional
from src.domains.professional.repository import ProfessionalRepository


class ProfessionalServices:
    @inject
    def __init__(self, repository: ProfessionalRepository):
        self._repository = repository

    async def fetch_by_professional_registration(self, professional_registration: str) -> Professional:
        return await self._repository.fetch_by_professional_registration(
            professional_registration=professional_registration
        )
