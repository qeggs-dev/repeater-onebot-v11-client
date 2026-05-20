from .._clients import ChatClient
from ...command_register import CommandCaller
from .._bases import BaseChat
from ...assist import PersonaInfo, SendMsg

@CommandCaller.register
class NoReason(BaseChat):
    cmd = "noReason"
    aliases = {
        "nr",
        "NR",
        "no_reason",
        "No_Reason",
        "NoReason",
        "NO_REASON"
    }
    documents = f"""
        Forces the use of non-inferential mode for text generation.
        
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
            thinking = False
        )
        return response