from ._chat_base_pkg import BaseChat
from .._clients import ChatSendMsg
from ...command_register import CommandCaller

@CommandCaller.register
class RenderChat(BaseChat):
    cmd = "renderChat"
    aliases = {
        "rc",
        "render_chat",
        "Render_Chat",
        "RenderChat"
    }
    component = "Chat.Render_Chat"

    async def send_chat_send_msg(
        self,
        chat_send_msg: ChatSendMsg,
    ):
        await chat_send_msg.send_image_mode()