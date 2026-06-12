from pydantic import BaseModel
from typing import Any
from .._content_role import ContentRole
from ._cross_user_data_routing import CrossUserDataRouting
from ...assist import PersonaInfo
from ...client_net_configs import storage_configs

class ChatUserInfo(BaseModel):
    username: str | None = None
    nickname: str | None = None
    age: int | float | None = None
    gender: str | None = None

class AdditionalData(BaseModel):
    image_url: str | list[str] | None = None
    video_url: str | list[str] | None = None
    audio_url: str | list[str] | None = None
    file_url: str | list[str] | None = None

class ChatRequestModel(BaseModel):
    message: str | None = None
    suffix: str | None = None
    echo: bool | None = None
    fim_mode: bool | None = None
    user_info: ChatUserInfo | None = None
    allow_tool_calls: bool | None = None
    add_metadata: bool = True
    role_name: str | None = None
    extra_template_fields: dict[str, Any] | None = None
    temporary_prompt: str | None = None
    model_id: str | None = None
    thinking: bool | None = None
    additional_data: AdditionalData | None = None
    load_prompt: bool | None = None
    save_context: bool | None = None
    save_new_only: bool | None = None
    history_msg_role_map: dict[ContentRole, ContentRole | None] | None = None
    cross_user_data_routing: CrossUserDataRouting | None = None
    continue_completion: bool | None = None
    stream: bool | None = None
    
    def submit_message(self) -> str | None:
        message_buffer:list[str] = []
        if self.add_metadata:
            message_buffer.append("> MessageMetadata:")
            message_buffer.append(">     Message Type: {{message_type}}")
            message_buffer.append(">     Message Sending time:{{time()}}")
            if storage_configs.usage_group_context:
                message_buffer.append(">     Now User: {{user_name}}({{nick_name}})")
            if self.cross_user_data_routing:
                message_buffer.append(">     Guest Mode(User: {{user_name}}), Citation context is turned on!!")
            message_buffer.append("\n---\n")
        message_buffer.append(self.message)
        return "\n".join(message_buffer)
    
    def submit_body(self) -> dict[str, Any]:
        base_body = self.model_dump(exclude_none=True)
        if self.message:
            base_body["message"] = self.submit_message()
        return base_body