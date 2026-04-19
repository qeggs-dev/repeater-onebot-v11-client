from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import PromptClient
from ....assist import PersonaInfo, SendMsg

get_prompt = on_command("getPrompt", aliases={"gp", "get_prompt", "Get_Prompt", "GetPrompt"}, rule=to_me(), block=True)


@get_prompt.handle()
async def handle_get_prompt(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Prompt.Get_Prompt", get_prompt, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    
    prompt_client = PromptClient(persona_info)
    response = await prompt_client.get_prompt()
    if response:
        if response.text:
            await send_msg.send_render_prompt(response.text)
        else:
            await send_msg.send_prompt("[No Prompt]")
    else:
        await send_msg.send_response(response)
