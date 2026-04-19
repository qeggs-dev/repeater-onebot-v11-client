from .._clients import ChatClient
from ._chat_base_pkg import BaseChat
from ...command_register import CommandCaller
from ...assist import PersonaInfo, SendMsg

@CommandCaller.register
class NPChat(BaseChat):
    cmd = "npChat"
    aliases = {
        "np",
        "no_prompt_chat",
        "No_Prompt_Chat",
        "NoPromptChat"
    }
    component = "Chat.No_Prompt_Chat"
    
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