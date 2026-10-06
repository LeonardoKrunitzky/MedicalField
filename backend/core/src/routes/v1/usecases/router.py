from fastapi import APIRouter


router = APIRouter(prefix="/usecases")

router.include_router(router, prefix="/usecases", tags=["Usecases"])