from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import ConfigCore
from ....assist import PersonaInfo, SendMsg, str_to_bool

allow_tool_calls = on_command("allowToolCalls", aliases={"atc", "allow_tool_calls", "Allow_Tool_Calls", "AllowToolCalls"}, rule=to_me(), block=True)

@allow_tool_calls.handle()
async def handle_tool_calls(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Config.Allow_Tool_Calls", allow_tool_calls, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    try:
        thinking = str_to_bool(persona_info.message_striped_str)
    except ValueError:
        await send_msg.send_error("Not a valid value")

    config_core = ConfigCore(persona_info)
    response = await config_core.set_config("allow_tool_calls", thinking)
    thinking_mode_str = "enabled" if thinking else "disabled"
    await send_msg.send_response_check_code(response, f"Thinking Mode is {thinking_mode_str}")