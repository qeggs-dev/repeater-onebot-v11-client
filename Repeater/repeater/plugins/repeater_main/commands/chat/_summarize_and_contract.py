from .._clients import ChatClient
from ...command_register import CommandCaller
from ._chat_base_pkg import BaseChat
from ...assist import PersonaInfo, SendMsg

@CommandCaller.register
class SummarizeAndContract(BaseChat):
    cmd = "summarizeAndContract"
    aliases = {
        "sac",
        "summarize_and_contract",
        "Summarize_And_Contract",
        "SummarizeAndContract"
    }
    component = "Chat.Summarize_And_Contract"
    
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
            save_new_only = True
        )
        return response