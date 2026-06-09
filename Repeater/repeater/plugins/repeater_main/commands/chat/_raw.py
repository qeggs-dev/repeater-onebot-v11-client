from .._clients import ChatClient
from ...assist import PersonaInfo, SendMsg
from ...command_register import CommandCaller
from .._bases import BaseChat

@CommandCaller.register
class RawChat(BaseChat):
    cmd = "raw"
    aliases = {
        "RAW",
        "rawchat",
        "raw_chat",
        "Raw_Chat",
        "RawChat",
        "RAW_CHAT"
    }
    documents = f"""
        Generates text without adding metadata.
        
        Usage:
        ```
        /{cmd} text
        ```
    """
    
    async def send_message(
        self,
        client: ChatClient,
        images: list[str],
        audios: list[str],
        videos: list[str],
        message: str,
        persona_info: PersonaInfo,
        send_msg: SendMsg
    ) -> str:
        response = await client.send_message(
            message = message,
            image_url = images,
            audio_url = audios,
            video_url = videos,
            add_metadata = False
        )
        return response