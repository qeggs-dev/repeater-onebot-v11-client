from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import ConfigClient
from ....assist import PersonaInfo, SendMsg, str_to_bool

set_remove_reasoning_prompt = on_command("removeReasoningPrompt", aliases={"rrp", "remove_reasoning_prompt", "Remove_Reasoning_Prompt", "RemoveReasoningPrompt"}, rule=to_me(), block=True)

@set_remove_reasoning_prompt.handle()
async def handle_set_remove_reasoning_prompt(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Config.Remove_Reasoning_Prompt", set_remove_reasoning_prompt, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    
    try:
        remove_reasoning_prompt = str_to_bool(persona_info.message_striped_str)
    except ValueError:
        await send_msg.send_error("Not a valid boolean value")
    
    config_client = ConfigClient(persona_info)
    response = await config_client.set_config("remove_reasoning_prompt", remove_reasoning_prompt)
    await send_msg.send_response_check_code(response, f"Set Remove Reasoning Prompt to {remove_reasoning_prompt}")
        
