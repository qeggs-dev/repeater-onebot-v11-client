from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ..._clients import PromptClient
from ....assist import PersonaInfo, FileSender, SendMsg

send_prompt_file = on_command("sendPromptFile", aliases={"spf", "send_prompt_file", "Send_Prompt_File", "SendPromptFile"}, rule=to_me(), block=True)

@send_prompt_file.handle()
async def handle_send_prompt_file(bot: Bot, event: MessageEvent):
    persona_info = PersonaInfo(bot=bot, event=event)
    send_msg = SendMsg("Prompt.Send_Prompt_File", send_prompt_file, persona_info)

    user_file_client = PromptClient(persona_info)
    file_url = user_file_client.get_prompt_url()
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        file_sender = FileSender(persona_info)

        await file_sender.send_file(file_url, f"{persona_info.namespace_str}_User_Prompt.md")
