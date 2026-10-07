from abc import ABC, abstractmethod
from uuid import UUID

from src.domains.medication.entity import Medication

class MedicationRepository(ABC):
    @abstractmethod
    async def register_medication(self, id: UUID, name: str, standard_dosage: str):
        """
         Create a new medication.

        :param id: The unique identifier of the medication.
        :param name: The name of the medication.
        :param standard_dosage: The standard dosage of the medication.
        """
        pass

    @abstractmethod
    async def fetch_medications(self) -> list[Medication]:
        """
        Fetch all medications.

        :return: A list of medication objects.
        """
        pass