from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import ConfigClient
from ....assist import PersonaInfo, SendMsg, parse_delimited_string

set_stop_keywords = on_command("setStopKeywords", aliases={"ssk", "set_stop_keywords", "Set_Stop_Keywords", "SetStopKeywords"}, rule=to_me(), block=True)

@set_stop_keywords.handle()
async def handle_set_stop_keywords(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Config.Set_Stop_Keywords", set_stop_keywords, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    msg = persona_info.message_striped_str
    model_uids = parse_delimited_string(msg)

    if not model_uids:
        await send_msg.send_error("Please enter at least one stop keywords.")

    config_client = ConfigClient(persona_info)
    response = await config_client.set_config("stop", model_uids)
    await send_msg.send_response_check_code(response, f"Set Stop Keywords to {', '.join(model_uids)}")