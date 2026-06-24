from ...clients import ChatClient
from ...command_register import CommandCaller
from .._bases import BaseChat
from ...assist import PersonaInfo, SendMsg

@CommandCaller.register
class NoSaveChat(BaseChat):
    cmd = "noSaveChat"
    aliases = {
        "nsc",
        "NSC",
        "no_save_chat",
        "NoSaveChat",
        "No_Save_Chat",
        "NO_SAVE_CHAT"
    }
    documents = f"""
        Temporarily send a message. (Not saved in the chat history)
        
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
            save_context = False
        )
        return response