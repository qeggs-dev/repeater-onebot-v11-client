from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import PromptClient
from ....assist import PersonaInfo, SendMsg

change_prompt_branch = on_command("changePromptBranch", aliases={"cpb", "change_prompt_branch", "Change_Prompt_Branch", "ChangePromptBranch"}, rule=to_me(), block=True)

@change_prompt_branch.handle()
async def handle_change_prompt_branch(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Prompt.Change_Prompt_Branch", change_prompt_branch, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    msg = args.extract_plain_text().strip()
    
    prompt_client = PromptClient(persona_info)
    response = await prompt_client.change_branch(msg)
    await send_msg.send_response_check_code(response, f"Change Prompt Branch to {msg}")