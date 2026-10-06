from abc import ABC, abstractmethod


class AuthenticationRepository(ABC):
    @abstractmethod
    async def login(self, username: str, password: str):
        """
        Authenticate a user with the given username and password.

        :param username: The username of the user.
        :param password: The password of the user.
        :return: A user object if authentication is successful, None otherwise.
        """
        pass