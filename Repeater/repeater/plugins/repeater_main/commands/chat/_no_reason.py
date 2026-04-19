from .._clients import ChatClient
from ...command_register import CommandCaller
from ._chat_base_pkg import BaseChat
from ...assist import PersonaInfo, SendMsg

@CommandCaller.register
class NoReason(BaseChat):
    cmd = "noReason"
    aliases = {
        "nr",
        "no_reason",
        "No_Reason",
        "NoReason"
    }
    component = "Chat.NoReason"
    
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