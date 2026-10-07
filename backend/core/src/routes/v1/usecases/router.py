from fastapi import APIRouter
from .professional.routes import router as professional
from .medication.routes import router as medication

router = APIRouter(prefix="/usecases")

router.include_router(professional)
router.include_router(medication)