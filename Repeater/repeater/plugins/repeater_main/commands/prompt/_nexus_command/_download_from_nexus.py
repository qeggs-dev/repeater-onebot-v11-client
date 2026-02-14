from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ..._clients import PromptCore
from ....assist import PersonaInfo, SendMsg

prompt_download_from_nexus = on_command("promptDownloadFromNexus", aliases={"pdfn", "prompt_download_from_nexus", "Prompt_Download_From_Nexus", "PromptDownloadFromNexus"}, rule=to_me(), block=True)

@prompt_download_from_nexus.handle()
async def handle_prompt_download_from_nexus(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Prompt.Download_From_Nexus", prompt_download_from_nexus, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    
    prompt_core = PromptCore(persona_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        try:
            response = await prompt_core.download_from_nexus(persona_info.message_str)
        except ValueError as e:
            await send_msg.send_error(
                f"Invalid UUID: {persona_info.message_str}"
            )

        if response.code == 200:
            data = response.get_data()
            if data is None:
                await send_msg.send_error("Unable to process data.")
            else:
                await send_msg.send_prompt(
                    f"Download successful."
                )
        else:
            await send_msg.send_response_check_code(response, "Unable to download prompt from Nexus.")