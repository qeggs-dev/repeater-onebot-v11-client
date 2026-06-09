from pydantic import BaseModel

class FileInfo(BaseModel):
    file: str
    url: str
    file_size: str
    file_name: str