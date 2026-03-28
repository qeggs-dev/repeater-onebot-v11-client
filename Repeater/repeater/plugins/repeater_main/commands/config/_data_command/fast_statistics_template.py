from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import ConfigCore
from ....assist import PersonaInfo, SendMsg, str_to_bool

fast_statistics_template = on_command("fastStatisticsTemplate", aliases={"fst", "fast_statistics_template", "Fast_Statistics_Template", "FastStatisticsTemplate"}, rule=to_me(), block=True)

@fast_statistics_template.handle()
async def handle_fast_statistics_template(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Config.Fast_Statistics_Template", fast_statistics_template, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        config_core = ConfigCore(persona_info)
        message = persona_info.message_striped_str
        response = await config_core.set_config("request_statistics_template", message)
        await send_msg.send_response_check_code(response, f"Fast Statistics Template set to {message}")