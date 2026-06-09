
from pydantic import BaseModel, Field
from .ping_provider_details import PingProviderDetails

class PingProviderResponse(BaseModel):
    success_count: int = 0
    average_time_spent: float = 0.0
    details: list[PingProviderDetails] = Field(default_factory=list)