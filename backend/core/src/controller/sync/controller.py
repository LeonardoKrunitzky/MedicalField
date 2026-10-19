from injector import inject

from src.dtos.sync.read import OfflineDbResponse
from src.use_cases.sync.fetch import FetchOfflineDataUseCase
from src.use_cases.sync.pull import PullFromDatabaseUseCase
from src.use_cases.sync.push import PushToDatabaseUseCase


class SyncController:
    @inject
    def __init__(
        self,
        pull_use_case: PullFromDatabaseUseCase,
        sync_use_case: PushToDatabaseUseCase,
        fetch_offline_data_use_case: FetchOfflineDataUseCase,
    ):
        self.pull_use_case = pull_use_case
        self.push_use_case = sync_use_case
        self.fetch_offline_data_use_case = fetch_offline_data_use_case

    async def pull_from_database(self):
        return await self.pull_use_case.execute()

    async def push_to_database(self):
        return await self.push_use_case.execute()

    async def fetch_offline_data(self) -> OfflineDbResponse:
        return await self.fetch_offline_data_use_case.execute()