from pydantic import BaseModel, Field

class AudioFiles(BaseModel):
    filename: str = ""
    url: str = ""

class TTSResponse(BaseModel):
    code: int = 0
    message: str = "ok"
    audio_files: list[AudioFiles] = Field(default_factory=list)