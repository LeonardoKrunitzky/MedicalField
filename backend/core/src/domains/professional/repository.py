from abc import ABC, abstractmethod
from uuid import UUID

from src.domains.professional.entity import Professional


class ProfessionalRepository(ABC):
    @abstractmethod
    async def fetch_by_professional_registration(self, professional_registration: str, password: str) -> Professional:
        pass

    @abstractmethod
    async def fetch_all(self) -> list[Professional]:
        """Busca todos os profissionais cadastrados."""
        pass