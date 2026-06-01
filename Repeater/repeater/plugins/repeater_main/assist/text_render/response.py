from pydantic import BaseModel

class RendedImage(BaseModel):
    image_url: str = ""
    file_uuid: str = ""
    style: str = ""
    timeout: float = 0.0
    text: str = ""
    created: float = 0.0
    created_ms: int = 0