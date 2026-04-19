from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import PromptClient
from ....assist import PersonaInfo, SendMsg

setprompt = on_command("setPrompt", aliases={"sp", "set_prompt", "Set_Prompt", "SetPrompt"}, rule=to_me(), block=True)


@setprompt.handle()
async def handle_set_prompt(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Prompt.Set_Prompt", setprompt, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    msg = persona_info.message_striped_str
    
    prompt_client = PromptClient(persona_info)
    response = await prompt_client.set_prompt(msg)
    await send_msg.send_response_check_code(response, f"Set Prompt {'successfully' if response.code == 200 else 'failed'}")
