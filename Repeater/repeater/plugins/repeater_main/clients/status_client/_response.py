from pydantic import BaseModel, Field

class StatusResponse(BaseModel):
    contains: bool = False
    tasks: dict[str, list[str]] = Field(default_factory=dict)

    def __bool__(self) -> bool:
        return self.contains and bool(self.tasks)