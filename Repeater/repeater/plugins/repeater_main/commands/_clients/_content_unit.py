from pydantic import BaseModel
from ._content_role import ContentRole

class ContentUnit(BaseModel):
    reasoning_content: str | None = None
    content: str = ""
    role: ContentRole = ContentRole.SYSTEM