from pydantic import BaseModel, Field

class ChatBuffer(BaseModel):
    reasoning: str = ""
    content: str = ""

    def __len__(self):
        return len(self.reasoning) + len(self.content)

class ChatBufferResponse(BaseModel):
    user_id: str = ""
    buffers: list[ChatBuffer] = Field(default_factory=list)

    def __len__(self):
        return sum(len(buffer) for buffer in self.buffers)