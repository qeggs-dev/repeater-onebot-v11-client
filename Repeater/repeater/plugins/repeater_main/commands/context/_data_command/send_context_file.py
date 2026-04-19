from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import ContextClient
from ....assist import PersonaInfo, FileSender, SendMsg

send_context_file = on_command("sendContextFile", aliases={"scf", "send_context_file", "Send_Context_File", "SendContextFile"}, rule=to_me(), block=True)

@send_context_file.handle()
async def handle_send_context_file(bot: Bot, event: MessageEvent):
    persona_info = PersonaInfo(bot=bot, event=event)
    send_msg = SendMsg("Context.Send_Context_File", send_context_file, persona_info)

    user_file_client = ContextClient(persona_info)
    file_url = user_file_client.get_context_url()
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        file_sender = FileSender(
            persona_info = persona_info,
            send_msg = send_msg
        )

        await file_sender.send_file(file_url, f"{persona_info.namespace_str}_User_Context.json")
