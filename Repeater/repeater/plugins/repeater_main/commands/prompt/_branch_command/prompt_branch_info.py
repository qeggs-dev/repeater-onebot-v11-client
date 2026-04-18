from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ..._clients import PromptClient
from ....assist import PersonaInfo, SendMsg

prompt_branch_info = on_command("promptBranchInfo", aliases={"pbi", "prompt_branch_info", "Prompt_Branch_Info", "PromptBranchInfo"}, rule=to_me(), block=True)

@prompt_branch_info.handle()
async def handle_prompt_branch_info(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Prompt.Prompt_Branch_Info", prompt_branch_info, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    
    prompt_client = PromptClient(persona_info)
    response = await prompt_client.branch_info()
    if response.code == 200:
        data = response.get_data()
        if data is None:
            await send_msg.send_error("Unable to process data.")

        text_buffer: list[str] = []
        text_buffer.append(f"Branch Type: Prompt")
        text_buffer.append(f"Branch ID: {data.branch_id}")
        if data.file_exists:
            text_buffer.append(f"Branch Size: {data.size}")
            text_buffer.append(f"Branch Readable Size: {data.readable_size}")
            text_buffer.append(f"Branch Last Modified Time: {data.modified_datetime().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            text_buffer.append("Branch File Not Exists")

        await send_msg.send_prompt("\n".join(text_buffer))
    else:
        await send_msg.send_response_check_code(response, "Get Prompt branch info failed")