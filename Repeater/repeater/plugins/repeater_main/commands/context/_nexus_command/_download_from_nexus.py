from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import ContextClient
from ....assist import PersonaInfo, SendMsg

context_download_from_nexus = on_command("contextDownloadFromNexus", aliases={"cdfn", "context_download_from_nexus", "Context_Download_From_Nexus", "ContextDownloadFromNexus"}, rule=to_me(), block=True)

@context_download_from_nexus.handle()
async def handle_context_download_from_nexus(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Context.Download_From_Nexus", context_download_from_nexus, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    
    context_client = ContextClient(persona_info)
    try:
        response = await context_client.download_from_nexus(persona_info.message_striped_str)
    except ValueError as e:
        await send_msg.send_error(
            f"Invalid UUID: {persona_info.message_striped_str}"
        )

    if response.code == 200:
        data = response.get_data()
        if data is None:
            await send_msg.send_error("Unable to process data.")
        else:
            await send_msg.send_prompt(f"Download successful.")
    else:
        await send_msg.send_response_check_code(response, "Unable to download context from Nexus.")