from ...clients import ChatClient, ChatResponse
from .._bases import BaseChat
from ...command_register import CommandCaller
from ...assist import PersonaInfo, SendMsg, Response

@CommandCaller.register
class NPChat(BaseChat):
    cmd = "npChat"
    aliases = {
        "np",
        "NP",
        "no_prompt_chat",
        "No_Prompt_Chat",
        "NoPromptChat",
        "NO_PROMPT_CHAT"
    }
    documents = f"""
        Generate the task without loading the prompt.
        
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
    ) -> Response[ChatResponse]:
        response: Response[ChatResponse] = await client.send_message(
            message = message,
            image_url = images,
            audio_url = audios,
            video_url = videos,
            load_prompt = False
        )
        return response