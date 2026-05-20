from pydantic import BaseModel, Field
from ._model_info import ModelInfo

class ModelsResponse(BaseModel):
    message: str = ""
    models: list[ModelInfo] = Field(default_factory=list)

class PingProviderDetails(BaseModel):
    host: str = ""
    time: list[float] = Field(default_factory=list)
    packet_loss: float = 0.0
    max_time: float = 0.0
    min_time: float = 0.0
    avg_time: float = 0.0

class PingProviderResponse(BaseModel):
    successful: int = 0
    average_time_spent: float = 0.0
    details: list[PingProviderDetails] = Field(default_factory=list)