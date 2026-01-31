from pydantic import BaseModel

class NexusUploadResponse(BaseModel):
    message: str = ""
    nexus_message: str = ""
    file_uuid: str | None = None

class NexusDownloadResponse(BaseModel):
    message: str = ""
    nexus_message: str = ""