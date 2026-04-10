from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ..._clients import PromptCore
from ....assist import PersonaInfo, SendMsg

prompt_upload_to_nexus = on_command("promptUploadToNexus", aliases={"putn", "prompt_upload_to_nexus", "Prompt_Upload_To_Nexus", "PromptUploadToNexus"}, rule=to_me(), block=True)

@prompt_upload_to_nexus.handle()
async def handle_prompt_upload_to_nexus(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Prompt.Upload_To_Nexus", prompt_upload_to_nexus, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    
    prompt_core = PromptCore(persona_info)

    timeout = None
    if persona_info.message_striped_str:
        try:
            timeout = int(persona_info.message_striped_str)
        except ValueError:
            await send_msg.send_error("Invalid timeout value")
    
    response = await prompt_core.upload_to_nexus(timeout)

    if response.code == 200:
        data = response.get_data()
        if data is None:
            await send_msg.send_error("Unable to process data.")
        else:
            await send_msg.send_prompt(
                f"Upload successful.\nFile ID: {data.resource_uuid}"
            )
    else:
        await send_msg.send_response_check_code(response, "Unable to upload prompt to Nexus.")