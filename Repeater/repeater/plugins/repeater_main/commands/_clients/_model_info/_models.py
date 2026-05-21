from pydantic import BaseModel, Field
from ._model_info import ModelInfo

class ModelsResponse(BaseModel):
    message: str = ""
    models: list[ModelInfo] = Field(default_factory=list)

class PingProviderDetails(BaseModel):
    host_names: list[str] = Field(default_factory=list)
    ip: str | None = None
    time: list[float] = Field(default_factory=list)
    packet_loss: float = 0.0
    max_time: float = 0.0
    min_time: float = 0.0
    avg_time: float = 0.0

class PingProviderResponse(BaseModel):
    success_count: int = 0
    average_time_spent: float = 0.0
    details: list[PingProviderDetails] = Field(default_factory=list)