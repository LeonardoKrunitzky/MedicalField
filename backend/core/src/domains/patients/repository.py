from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from src.domains.patients.entity import Patient

class PatientRepository(ABC):
    @abstractmethod
    async def create(self, name: str, document: str, created_at: datetime) -> Patient:
        """
        Create a new patient.
        :return: A dictionary representing the created patient.
        """
        pass

    @abstractmethod
    async def fetch_all(self) -> list[Patient]:
        """
        Fetch all patients.
        :return: A list of patient dictionaries.
        """
        pass

    @abstractmethod
    async def fetch_by_id(self, patient_id: UUID) -> Patient:
        """
        Fetch a patient by ID.
        :return: A dictionary representing the patient.
        """
        pass

class PatientOfflineRepository(ABC):
    @abstractmethod
    async def save_patient_offline(self, id: UUID, name: str, document: str, created_at: datetime) -> Patient:
        """
        Create a new patient.
        :return: A dictionary representing the created patient.
        """
        pass