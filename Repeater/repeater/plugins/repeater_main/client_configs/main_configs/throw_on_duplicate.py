from pydantic import BaseModel

class ThrowOnDuplicate(BaseModel):
    trigger: bool = True
    handler: bool = True