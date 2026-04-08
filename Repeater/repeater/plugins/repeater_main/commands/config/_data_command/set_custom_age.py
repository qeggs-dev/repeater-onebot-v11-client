from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import ConfigCore
from ....assist import PersonaInfo, SendMsg, str_to_bool

set_custom_age = on_command("setCustomAge", aliases={"sca", "set_custom_age", "Set_Custom_Age", "SetCustomAge"}, rule=to_me(), block=True)

@set_custom_age.handle()
async def handle_set_custom_age(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Config.Set_Custom_Age", set_custom_age, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        config_core = ConfigCore(persona_info)
        response = await config_core.set_config("user_age", persona_info.message_striped_str)
        await send_msg.send_response_check_code(response, f"Custom Age seted")