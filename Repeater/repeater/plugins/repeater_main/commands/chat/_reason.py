from ...assist import PersonaInfo, SendMsg
from .._clients import ChatClient
from ...command_register import CommandCaller
from .._bases import BaseChat

@CommandCaller.register
class Reason(BaseChat):
    cmd = "reason"
    aliases = {
        "r",
        "R",
        "Reason",
        "REASON"
    }
    documents = f"""
        The inference mode is forced to be turned on for this text generation task.
        
        Usage:
        ```
        /{cmd} [text]
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
            thinking = True
        )
        return response