from abc import ABC, abstractmethod

class SyncConflictStrategy(ABC):
    @abstractmethod
    def resolve(self, local_record: dict, server_record: dict) -> dict:
        pass
