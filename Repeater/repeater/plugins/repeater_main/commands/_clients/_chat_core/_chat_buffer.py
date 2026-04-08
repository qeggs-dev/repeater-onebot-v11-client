from pydantic import BaseModel

class ChatBuffer(BaseModel):
    reasoning: str = ""
    content: str = ""