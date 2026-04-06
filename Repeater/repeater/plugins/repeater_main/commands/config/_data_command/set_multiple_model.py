from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import ConfigCore
from ....assist import PersonaInfo, SendMsg, parse_delimited_string

set_multiple_model = on_command("setMultipleModel", aliases={"smm", "set_multiple_model", "Set_Multiple_Model", "SetMultipleModel"}, rule=to_me(), block=True)

@set_multiple_model.handle()
async def handle_set_multiple_model(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Config.Set_Multiple_Model", set_multiple_model, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    msg = persona_info.message_striped_str
    model_uids = parse_delimited_string(msg)

    if not model_uids:
        await send_msg.send_error("Please enter at least one model_uid")

    config_core = ConfigCore(persona_info)
    response = await config_core.set_config("model_uid", model_uids)
    await send_msg.send_response_check_code(response, f"Set Multiple Model to {', '.join(model_uids)}")