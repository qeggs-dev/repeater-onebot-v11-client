from pydantic import BaseModel

class ChatBuffer(BaseModel):
    reasoning: str = ""
    content: str = ""

    def __len__(self):
        return len(self.reasoning) + len(self.content)