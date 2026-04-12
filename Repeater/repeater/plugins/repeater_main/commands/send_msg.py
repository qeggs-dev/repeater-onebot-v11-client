import json

from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ..assist import PersonaInfo, SendMsg
from pydantic import ValidationError
from ..core_net_configs import storage_configs

send_message = on_command("sendMessage", aliases={"smsg", "send_message", "Send_Message", "SendMessage"}, rule=to_me(), block=True)

@send_message.handle()
async def handle_send_message(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot, event, args)
    send_msg = SendMsg("Send.Send_Message", send_message, persona_info)

    if not storage_configs.allow_send_any_message:
        await send_msg.send_error("Send_Message is disabled")
    
    try:
        message_body = json.loads(persona_info.message_striped_str)
    except json.JSONDecodeError:
        await send_msg.send_error("Send_Message must enter a valid JSON")
    
    try:
        if isinstance(message_body, list):
            message_body = [MessageSegment(segment) for segment in message_body]
        elif isinstance(message_body, str):
            message_body = MessageSegment.text(message_body)
        elif isinstance(message_body, dict):
            message_body = MessageSegment(message_body)
        else:
            await send_msg.send_error("Please enter the correct content format.")
            return
        
        message = Message(message_body)
    except ValidationError as e:
        errors = e.errors()
        text_buffer: list[str] = []
        for error in errors:
            error_text = f"{'.'.join(error['loc'])}: {error['msg']}"
            text_buffer.append(error_text)
        await send_msg.send_error("\n".join(text_buffer))
    
    await send_msg.send_any(
        message,
        reply = False
    )