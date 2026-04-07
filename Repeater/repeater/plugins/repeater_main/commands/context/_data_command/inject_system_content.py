from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import ContextCore, ContentRole, ContentUnit
from ....assist import PersonaInfo, SendMsg

inject_system_content = on_command("injectSystemContent", aliases={"isc", "inject_system_content", "Inject_System_Content", "InjectSystemContent"}, rule=to_me(), block=True)

@inject_system_content.handle()
async def handle_inject_system_content(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Context.Inject_System_Content", inject_system_content, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    
    context_core = ContextCore(persona_info)
    response = await context_core.inject_context(
        content_unit = ContentUnit(
            content = persona_info.message_striped_str,
            role = ContentRole.SYSTEM
        )
    )

    if response:
        await send_msg.send_response(
            response,
            message = "Inject System Content Successful"
        )
    else:
        await send_msg.send_response(
            response,
            message = "Inject System Content Failed"
        )