from fastapi import APIRouter, Depends
from fastapi_injector import Injected
from src.config.security.security import verify_token
from src.controller.sync.controller import SyncController
from src.dtos.sync.read import OfflineDbResponse

router = APIRouter(
    prefix="/core/usecases/sync",
    tags=["Offline & Sync (SQLite)"],
    dependencies=[Depends(verify_token)],
)


@router.post(
    "/pull", summary="Baixa dados do PostgreSQL para o SQLite local (Passos 6 e 11)"
)
async def pull_data(controller: SyncController = Injected(SyncController)):
    return await controller.pull_from_database()


@router.post(
    "/push", summary="Envia dados pendentes do SQLite para o PostgreSQL (Passo 14)"
)
async def push_data(controller: SyncController = Injected(SyncController)):
    return await controller.push_to_database()

@router.get(
    "/fetchOfflineData",
    summary="Fetch offline data",
    status_code=200,
    response_model=OfflineDbResponse,
    responses={
        401: {"description": "Credenciais inválidas (registro ou senha)"},
        500: {"description": "Erro interno no servidor"},
    },
)
async def fetch_offline_data(
    controller: SyncController = Injected(SyncController),
):
    return await controller.fetch_offline_data()