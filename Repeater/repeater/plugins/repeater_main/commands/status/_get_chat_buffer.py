from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot
from typing import Any

from .._clients import ChatCore
from ...assist import PersonaInfo, SendMsg, str_to_bool

get_chat_buffer = on_command("getChatBuffer", aliases={"gcb", "get_chat_buffer", "Get_Chat_Buffer", "GetChatBuffer"}, rule=to_me(), block=True)

@get_chat_buffer.handle()
async def handle_get_chat_buffer(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Status.Get_Chat_Buffer", get_chat_buffer, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        chat_core = ChatCore(persona_info)
        response = await chat_core.get_chat_buffer()
        if response:
            buffer = response.get_data()
            if buffer is None:
                await send_msg.send_error(response.get_error())
            else:
                await send_msg.send_chat_response(
                    reasoning_content = buffer.reasoning,
                    content = buffer.content
                )