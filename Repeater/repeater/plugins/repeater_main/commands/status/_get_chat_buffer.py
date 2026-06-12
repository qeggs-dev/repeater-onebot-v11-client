from ...assist import PersonaInfo, SendMsg, CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ...clients import ChatClient


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
    cmd_type = CmdTypes.STATUS

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        chat_client = ChatClient(persona_info)
        response = await chat_client.get_chat_buffer()
        if response:
            buffer_response = response.get_data()
            if buffer_response is None:
                await send_msg.send_error(response.get_error())
            else:
                for task_id, buffer in buffer_response.buffers.items():
                    await send_msg.send_chat_response(
                        reasoning_content = buffer.reasoning,
                        content = buffer.content,
                        continue_handler = True
                    )
        
        send_msg.break_handler()