from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import ConfigClient
from ....assist import PersonaInfo, SendMsg, str_to_bool

thinking_mode = on_command("thinkingMode", aliases={"tm", "thinking_mode", "Thinking_Mode", "ThinkingMode"}, rule=to_me(), block=True)

@thinking_mode.handle()
async def handle_thinking_mode(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Config.Thinking_Mode", thinking_mode, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    try:
        thinking = str_to_bool(persona_info.message_striped_str, optional = True)
    except ValueError:
        await send_msg.send_error("Not a valid value")

    config_client = ConfigClient(persona_info)
    response = await config_client.set_config("thinking", thinking)
    if thinking is None:
        thinking_mode_str = "default"
    else:
        thinking_mode_str = "enabled" if thinking else "disabled"
    await send_msg.send_response_check_code(response, f"Thinking Mode is {thinking_mode_str}")