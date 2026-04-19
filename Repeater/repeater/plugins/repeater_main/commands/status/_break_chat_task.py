from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from .._clients import ChatClient
from ...assist import PersonaInfo, SendMsg

break_chat_task = on_command("breakChatTask", aliases={"bct", "break_chat_task", "Break_Chat_Task", "BreakChatTask"}, rule=to_me(), block=True)

@break_chat_task.handle()
async def handle_break_chat_task(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Status.Break_Chat_Task", break_chat_task, persona_info)

    core = ChatClient(persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        response = await core.break_chat_task()
        if response.code == 200:
            break_response = response.get_data()
            if break_response is None:
                await send_msg.send_error("Failed parsing response data.")
            else:
                await send_msg.send_prompt(break_response.msg)
        else:
            await send_msg.send_error_response(response)