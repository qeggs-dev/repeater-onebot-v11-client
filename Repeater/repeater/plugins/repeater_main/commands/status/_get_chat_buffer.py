from ...assist import PersonaInfo, SendMsg
from ...command_register import(
    CommandCaller,
    CommandPackage,
    CmdType
)
from .._clients import ChatClient


@CommandCaller.register
class GetChatBuffer(CommandPackage):
    cmd = "getChatBuffer"
    aliases = {
        "gcb",
        "GCB",
        "get_chat_buffer",
        "Get_Chat_Buffer",
        "GetChatBuffer",
        "GET_CHAT_BUFFER",
    }
    type = CmdType.STATUS

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        chat_client = ChatClient(persona_info)
        response = await chat_client.get_chat_buffer()
        if response:
            buffer = response.get_data()
            if buffer is None:
                await send_msg.send_error(response.get_error())
            else:
                await send_msg.send_chat_response(
                    reasoning_content=buffer.reasoning,
                    content=buffer.content
                )