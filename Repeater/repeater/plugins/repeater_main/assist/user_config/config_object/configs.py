from pydantic import BaseModel

class UserConfigs(BaseModel):
    backend: str | None = None