from nonebot import get_plugin_config
from pydantic import BaseModel

class ChatConfig(BaseModel):
    backend_baseurl: str = "http://127.0.0.1"
    repeater_debug_mode: bool = False

net_config: ChatConfig = get_plugin_config(ChatConfig)