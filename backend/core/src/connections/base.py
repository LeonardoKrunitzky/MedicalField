from abc import ABC, abstractmethod


class BaseClient(ABC):
    """
    Base contract for infrastructure clients managed by the application infrastructure lifecycle.
    """

    @abstractmethod
    async def connect(self) -> None:
        """Establish the connection to the external service."""

    @abstractmethod
    async def disconnect(self) -> None:
        """Gracefully close the connection."""

    @abstractmethod
    async def ensure_connected(self) -> None:
        """Ensure the client is connected or raise a startup error."""
