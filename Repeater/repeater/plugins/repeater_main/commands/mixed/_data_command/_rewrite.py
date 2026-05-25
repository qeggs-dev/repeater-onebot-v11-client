from nonebot import logger
from ....assist import PersonaInfo, SendMsg
from ....command_register import(
    CommandCaller,
    CmdTypes
)
from ....storage import async_text_storage
from ..._clients import ContextClient, ChatClient
from ..._bases import BaseChat
from ._default_meta_prompt import META_PROMPT


@CommandCaller.register
class Rewrite(BaseChat):
    cmd = "rewrite"
    aliases = {
        "rew",
        "REW",
        "Rewrite",
        "REWRITE",
    }
    cmd_type = CmdTypes.MIXED
 
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
        context_client = ContextClient(persona_info)
        response = await context_client.withdraw()
        
        if response:
            data = response.get_data()
            if data is None:
                await send_msg.send_error(
                    "Unable to process data."
                )
                return
            await send_msg.send_prompt(
                (
                    f"Deleted: {data.deleted}\n"
                    f"Remaining: {len(data.context)}\n"
                ),
                continue_handler = True
            )
        else:
            await send_msg.send_response_check_code(response, "Withdraw Failed")
        
        return await super().send_message(
            client,
            images,
            audios,
            videos,
            message,
            persona_info,
            send_msg
        )