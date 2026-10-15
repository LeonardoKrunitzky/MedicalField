from abc import ABC, abstractmethod
from uuid import UUID

from src.domains.medication.entity import Medication

class MedicationRepository(ABC):
    @abstractmethod
    async def fetch_medications(self) -> list[Medication]:
        """
        Fetch all medications.

        :return: A list of medication objects.
        """
        pass