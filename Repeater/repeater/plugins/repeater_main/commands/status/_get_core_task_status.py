from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot
from typing import Any

from .._clients import StatusCore
from ...assist import PersonaInfo, SendMsg, str_to_bool

get_core_task_status = on_command("getCoreTaskStatus", aliases={"gcts", "get_core_task_status", "Get_Core_Task_Status", "GetCoreTaskStatus"}, rule=to_me(), block=True)

@get_core_task_status.handle()
async def handle_get_core_task_status(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Status.Get_Core_Task_Status", get_core_task_status, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        status_core = StatusCore()
        response = await status_core.get_core_task_status(persona_info.namespace_str)
        if response.code == 200:
            status_stack: list[str] | Any = response.json()
            if not isinstance(status_stack, list):
                await send_msg.send_error("Response data is not a list")
            elif not status_stack:
                await send_msg.send_prompt("Free")
            else:
                text_buffer: list[str] = []
                for index, status in enumerate(status_stack):
                    if index == 0:
                        prefix = ""
                    else:
                        prefix = ("  " * index) + "└ "
                    text_buffer.append(prefix + status)
                
                await send_msg.send_check_length_prompt("\n".join(text_buffer))
        else:
            await send_msg.send_response_check_code(response)

