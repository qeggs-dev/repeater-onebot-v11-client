from pydantic import BaseModel, Field
from datetime import datetime
from ._content_role import ContentRole
from ._function_calling_response import CallingRequest

class ContentUnit(BaseModel):
    reasoning_content: str | None = None
    content: str = ""
    role: ContentRole = ContentRole.SYSTEM
    role_name: str |  None = None
    prefix: bool | None = None
    created: datetime = Field(default_factory=datetime.now)
    tool_calls: list[CallingRequest] | None = None
    tool_call_id: str | None = None