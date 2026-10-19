from injector import inject

from src.dtos.professional.read import ReadAllProfessionalsResponseDTO
from src.services.professional.service import ProfessionalService

class FetchAllProfessionalsUseCase:
    @inject
    def __init__(self, professional_service: ProfessionalService):
        self.professional_service = professional_service

    async def execute(self) -> ReadAllProfessionalsResponseDTO:
        try:
            results = await self.professional_service.fetch_all()
            return ReadAllProfessionalsResponseDTO(items=results)
        except Exception as e:
            raise ValueError(f"Fetch all professionals failed: {str(e)}")