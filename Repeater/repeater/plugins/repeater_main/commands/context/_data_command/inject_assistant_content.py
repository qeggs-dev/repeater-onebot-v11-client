from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import ContextCore, ContentRole
from ....assist import PersonaInfo, SendMsg

inject_assistant_content = on_command("injectAssistantContent", aliases={"iuc", "inject_assistant_content", "Inject_Assistant_Content", "InjectAssistantContent"}, rule=to_me(), block=True)

@inject_assistant_content.handle()
async def handle_inject_assistant_content(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Context.Inject_Assistant_Content", inject_assistant_content, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    
    context_core = ContextCore(persona_info)
    response = await context_core.inject_context(
        content = persona_info.message_striped_str,
        role = ContentRole.ASSISTANT
    )

    if response:
        await send_msg.send_prompt("Inject Assistant Content Successful")
    else:
        await send_msg.send_error("Inject Assistant Content Failed")