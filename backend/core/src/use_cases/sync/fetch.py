from injector import inject

from src.dtos.sync.read import OfflineDbResponse
from src.services.sync.service import SyncService


class FetchOfflineDataUseCase:
    @inject
    def __init__(self, sync_service: SyncService):
        self.sync_service = sync_service

    async def execute(self):
        try:
            response = await self.sync_service.fetch_offline_data()
            return OfflineDbResponse(
                attendances=response["attendances"],
                medical_records=response["medical_records"],
                patients=response["patients"],
                medications=response["medications"],
            )
        except Exception as e:
            print(e)