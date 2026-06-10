import re
from .._bases import BaseChat
from ...assist import PersonaInfo
from .._clients import ChatClient
from ...command_register import CommandCaller

@CommandCaller.register
class ToPrivateChat(BaseChat):
    cmd = "toPrivateChat"
    aliases = {
        "tpc",
        "TPC",
        "to_private_chat",
        "To_Private_Chat",
        "ToPrivateChat",
        "TO_PRIVATE_CHAT"
    }
    documents = f"""
        Send a build request as a private chat.
        
        Usage:
        ```
        /{cmd} text
        ```
    """
    
    def get_client(self, persona_info: PersonaInfo) -> ChatClient:
        client = ChatClient(
            persona_info,
            namespace = persona_info.private_namespace,
        )
        return client