from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Professional(BaseModel):
    id: UUID
    name: str
    professional_registration: str
    password: str
    created_at: datetime