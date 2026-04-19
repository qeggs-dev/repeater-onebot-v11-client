from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import ContextClient, PromptClient, ConfigClient
from ....assist import PersonaInfo, SendMsg

session_branch_bind = on_command("sessionBranchBind", aliases={"sbb", "session_branch_bind", "Session_Branch_Bind", "SessionBranchBind"}, rule=to_me(), block=True)

@session_branch_bind.handle()
async def handle_session_branch_bind(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Session.Session_Branch_Bind", session_branch_bind, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    msg = args.extract_plain_text().strip()
    
    context_client = ContextClient(persona_info)
    prompt_client = PromptClient(persona_info)
    config_client = ConfigClient(persona_info)
    
    context_response = await context_client.bind(msg)
    prompt_response = await prompt_client.bind(msg)
    config_response = await config_client.bind(msg)

    await send_msg.send_multiple_responses(
        (context_response, "Context"),
        (prompt_response, "Prompt"),
        (config_response, "Config"),
    )