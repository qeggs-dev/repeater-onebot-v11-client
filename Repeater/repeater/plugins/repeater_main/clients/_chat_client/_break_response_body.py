from pydantic import BaseModel

class BreakResponse(BaseModel):
    code: int = 200
    msg: str = ""
    cancel_count: int = 0