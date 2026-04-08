from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import ContextCore
from ....assist import PersonaInfo, SendMsg

get_last_content = on_command("getLastContent", aliases={"glc", "get_last_content", "Get_Last_Content", "GetLastContent"}, rule=to_me(), block=True)

@get_last_content.handle()
async def handle_get_last_content(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Context.Get_Last_Content", get_last_content, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        context_core = ContextCore(persona_info)

        response = await context_core.get_context()
        if response.code == 200:
            context = response.get_data()
            if context is None:
                await send_msg.send_error("Error: No Context Data")
            elif len(context) > 0:
                last_content = context[-1]
                await send_msg.send_chat_response(
                    last_content.reasoning_content,
                    last_content.content
                )
            else:
                await send_msg.send_error("Error: Context Data is Empty")
        else:
            await send_msg.send_response_check_code(response)

