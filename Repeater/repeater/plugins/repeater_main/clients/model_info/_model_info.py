from pydantic import BaseModel

class ModelInfo(BaseModel):
    name: str = ""
    parent: str = ""
    parent_id: str = ""
    uid: str = ""
    timeout: float = 600.0