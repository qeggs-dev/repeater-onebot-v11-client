import json
import yaml

from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import ConfigCore
from ....assist import PersonaInfo, SendMsg
from enum import StrEnum

get_configs = on_command("getConfigs", aliases={"gcfg", "get_configs", "Get_Configs", "GetConfigs"}, rule=to_me(), block=True)

class FormatType(StrEnum):
    JSON = "json"
    YAML = "yaml"

@get_configs.handle()
async def handle_get_configs(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Config.Get_Configs", get_configs, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    try:
        format_type = FormatType(persona_info.message_striped_str.lower())
    except ValueError:
        await send_msg.send_error("Format type is not supported. Please use 'json' or 'yaml'.")
    
    config_core = ConfigCore(persona_info)
    response = await config_core.get_configs()
    if response:
        try:
            match format_type:
                case FormatType.JSON:
                    await send_msg.send_check_length_prompt(json.dumps(response.json(), ensure_ascii=False, indent=4))
                case FormatType.YAML:
                    await send_msg.send_check_length_prompt(yaml.safe_dump(response.json(), allow_unicode=True))
        except json.JSONDecodeError as e:
            await send_msg.send_error(f"Failed to decode JSON: {e}")
    else:
        await send_msg.send_response(response, "Failed to get configs.")