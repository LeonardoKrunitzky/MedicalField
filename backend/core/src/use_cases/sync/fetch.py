from fastapi import HTTPException, status
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
                attendances=response["attendances"]["items"],
                medical_records=response["medical_records"]["items"],
                patients=response["patients"]["items"],
                medications=response["medications"]["items"],
            )
        except Exception as e:
            print(f"Erro real do SQLite: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Falha ao buscar dados offline: {str(e)}"
            )