from abc import abstractmethod


class SyncRepository:
    @abstractmethod
    async def pull_from_database(self):
        pass

    @abstractmethod
    async def push_to_database(self):
        pass

    @abstractmethod
    async def fetch_offline_data(self):
        pass