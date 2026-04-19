from .._clients import ChatClient
from ...assist import PersonaInfo
from ._chat_base_pkg import BaseChat
from ...command_register import CommandCaller

@CommandCaller.register
class PublicSpaceChat(BaseChat):
    cmd = "publicSpaceChat"
    aliases = {
        "psc",
        "public_space_chat",
        "Public_Space_Chat",
        "PublicSpaceChat"
    }
    component = "Chat.PublicSpaceChat"

    def get_client(self, persona_info: PersonaInfo):
        return ChatClient(persona_info, persona_info.public_namespace_str)