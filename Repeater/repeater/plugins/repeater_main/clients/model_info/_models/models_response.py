
from pydantic import BaseModel, Field
from .._model_info import ModelInfo

class ModelsResponse(BaseModel):
    message: str = ""
    models: list[ModelInfo] = Field(default_factory=list)