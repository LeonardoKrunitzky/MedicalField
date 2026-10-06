from fastapi import APIRouter
from .professional.professional import router as professional

router = APIRouter(prefix="/usecases")

router.include_router(professional)