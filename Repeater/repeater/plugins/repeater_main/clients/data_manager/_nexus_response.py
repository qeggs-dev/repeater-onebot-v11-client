from pydantic import BaseModel
from typing import Any

class NexusUploadResponse(BaseModel):
    message: str = ""
    nexus_message: str | Any = ""
    resource_uuid: str | None = None

class NexusDownloadResponse(BaseModel):
    message: str = ""
    nexus_message: str | Any = ""