from nonebot import get_plugin_config
from pydantic import BaseModel

class ChatConfig(BaseModel):
    repeater_debug_mode: bool = False

net_config: ChatConfig = get_plugin_config(ChatConfig)