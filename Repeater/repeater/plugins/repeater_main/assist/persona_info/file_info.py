from pydantic import BaseModel

class FileInfo(BaseModel):
    """
    文件信息
    """
    file: str
    url: str
    file_size: str
    file_name: str