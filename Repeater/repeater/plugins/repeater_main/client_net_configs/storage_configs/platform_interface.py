from pydantic import BaseModel

class PlatformInterface(BaseModel):
    cache: bool = True
    cache_size: int | float = 1000
    cache_timeout: int | float = 60