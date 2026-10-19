from injector import inject

from src.services.sync.service import SyncService


class PullFromDatabaseUseCase:
    @inject
    def __init__(self, sync_service: SyncService):
        self.sync_service = sync_service

    async def execute(self):
        try:
            await self.sync_service.pull_from_database()
        except Exception as e:
            print(e)