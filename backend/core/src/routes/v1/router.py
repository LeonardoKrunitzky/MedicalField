from fastapi import APIRouter
from .usecases.router import router as use_cases

router = APIRouter(prefix="/core", tags=["Core"])

router.include_router(use_cases)