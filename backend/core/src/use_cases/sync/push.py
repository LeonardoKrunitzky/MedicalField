from injector import inject

from src.services.sync.service import SyncService


class PushToDatabaseUseCase:
    @inject
    def __init__(self, sync_service: SyncService):
        self.sync_service = sync_service

    async def execute(self):
        try:
            await self.sync_service.push_to_database()
        except Exception as e:
            print(e)