from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import ConfigClient
from ....assist import PersonaInfo, SendMsg

set_custom_gender = on_command("setCustomGender", aliases={"scg", "set_custom_gender", "Set_Custom_Gender", "SetCustomGender"}, rule=to_me(), block=True)

@set_custom_gender.handle()
async def handle_set_custom_gender(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Config.Set_Custom_Gender", set_custom_gender, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        config_client = ConfigClient(persona_info)
        response = await config_client.set_config("user_gender", persona_info.message_striped_str)
        await send_msg.send_response_check_code(response, f"Custom Gender seted")