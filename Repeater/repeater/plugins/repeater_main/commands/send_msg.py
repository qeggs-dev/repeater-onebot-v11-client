import json

from nonebot.adapters.onebot.v11 import Message, MessageSegment
from pydantic import ValidationError

from ..assist import PersonaInfo, SendMsg
from ..command_register import(
    CommandCaller,
    CommandPackage,
    CmdTypes
)
from ..client_net_configs import storage_configs


@CommandCaller.register
class SendMessage(CommandPackage):
    cmd = "sendMessage"
    aliases = {
        "smsg",
        "SMSG",
        "send_message",
        "Send_Message",
        "SendMessage",
        "SEND_MESSAGE",
    }
    cmd_type = CmdTypes.SENDMSG

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        if not storage_configs.allow_send_any_message:
            await send_msg.send_error("Send_Message is disabled")
            return

        try:
            message_body = json.loads(persona_info.message_striped_str)
        except json.JSONDecodeError:
            await send_msg.send_error("Send_Message must enter a valid JSON")
            return

        try:
            if isinstance(message_body, list):
                message_body = [MessageSegment(**segment) for segment in message_body]
            elif isinstance(message_body, str):
                message_body = MessageSegment.text(message_body)
            elif isinstance(message_body, dict):
                message_body = MessageSegment(**message_body)
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
            return
        except Exception as e:
            await send_msg.send_error(str(e))
            return

        await send_msg.send_any(message, reply=False)