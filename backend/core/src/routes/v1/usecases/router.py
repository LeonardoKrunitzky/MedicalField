from fastapi import APIRouter
from .attendance.routes import router as attendance
from .medical_record.routes import router as medical_record
from .medication.routes import router as medication
from .patient.routes import router as patient
from .professional.routes import router as professional
from .sync.routes import router as sync

router = APIRouter(prefix="/usecases")

router.include_router(attendance)
router.include_router(medical_record)
router.include_router(medication)
router.include_router(patient)
router.include_router(professional)
router.include_router(sync)