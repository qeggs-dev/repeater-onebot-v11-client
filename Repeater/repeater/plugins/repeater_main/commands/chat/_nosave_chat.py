from .._clients import ChatClient
from ...command_register import CommandCaller
from ._chat_base_pkg import BaseChat
from ...assist import PersonaInfo, SendMsg

@CommandCaller.register
class NoSaveChat(BaseChat):
    cmd = "noSaveChat"
    aliases = {
        "nsc",
        "no_save_chat",
        "NoSaveChat",
        "No_Save_Chat"
    }
    component = "Chat.NoSaveChat"
    
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
            save_context = False
        )
        return response