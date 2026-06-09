from pydantic import BaseModel, Field

class ChatBuffer(BaseModel):
    reasoning: str = ""
    content: str = ""

    def __len__(self):
        return len(self.reasoning) + len(self.content)

class ChatBufferResponse(BaseModel):
    user_id: str = ""
    buffers: dict[str, ChatBuffer] = Field(default_factory=dict)

    def __len__(self):
        return sum(len(buffer) for buffer in self.buffers.values())