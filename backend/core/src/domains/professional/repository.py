from abc import ABC, abstractmethod
from uuid import UUID


class ProfessionalRepository(ABC):
    @abstractmethod
    async def create(self, id: UUID, name: str, professional_registration: str, password: str):
        """
        Create a new user with the given username and password.

        :param username: The username of the user.
        :param password: The password of the user.
        :return: A user object.
        """
        pass

    @abstractmethod
    async def read_by_professional_registration(self, professional_registration: str, password: str):
        """
        Read a user with the given username and password.

        :param username: The username of the user.
        :param password: The password of the user.
        :return: A user object.
        """
        pass