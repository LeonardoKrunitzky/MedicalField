from uuid import UUID

from injector import inject

from src.domains.sync.repository import SyncRepository



class SyncService:
    @inject
    def __init__(self, repository: SyncRepository):
        self._repository = repository

    async def pull_from_database(self):
        return await self._repository.pull_from_database()

    async def push_to_database(self):
        return await self._repository.push_to_database()

    async def fetch_offline_data(self):
        return await self._repository.fetch_offline_data()