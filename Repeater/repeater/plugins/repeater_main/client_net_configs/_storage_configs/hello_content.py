from pydantic import BaseModel, Field

class HelloSuffix(BaseModel):
    cron: str = ""
    content: str = ""

class HelloContent(BaseModel):
    content: str = "Repeater Is Ready!"
    suffixs: list[HelloSuffix] = Field(default_factory=list)