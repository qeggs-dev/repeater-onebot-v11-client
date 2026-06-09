from .._clients import ChatClient
from ...command_register import CommandCaller
from .._bases import BaseChat
from ...assist import PersonaInfo, SendMsg

@CommandCaller.register
class SummarizeAndContract(BaseChat):
    cmd = "summarizeAndContract"
    aliases = {
        "sac",
        "SAC",
        "summarize_and_contract",
        "Summarize_And_Contract",
        "SummarizeAndContract",
        "SUMARAIZE_AND_CONTRACT"
    }
    documents = f"""
        Summarizes the user's contextual content
        And save only summary information

        Usage:
        ```
        /{cmd} [message]
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
        if not message:
            return "Please provide a message to summarize"
        response = await client.send_message(
            message = message,
            image_url = images,
            audio_url = audios,
            video_url = videos,
            save_new_only = True
        )
        return response