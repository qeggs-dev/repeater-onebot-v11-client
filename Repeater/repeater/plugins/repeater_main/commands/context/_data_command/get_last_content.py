from ....assist import PersonaInfo, SendMsg
from ....command_register import(
    CommandCaller,
    CommandPackage,
    CmdType
)
from ..._clients import ContextClient


@CommandCaller.register
class GetLastContent(CommandPackage):
    cmd = "getLastContent"
    aliases = {
        "glc",
        "GLC",
        "get_last_content",
        "Get_Last_Content",
        "GetLastContent",
        "GET_LAST_CONTENT",
    }
    type = CmdType.CONTEXT

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        context_client = ContextClient(persona_info)

        response = await context_client.get_context()
        if response.code == 200:
            context = response.get_data()
            if context is None:
                await send_msg.send_error("Error: No Context Data")
            elif len(context) > 0:
                last_content = context[-1]
                await send_msg.send_chat_response(
                    last_content.reasoning_content,
                    last_content.content
                )
            else:
                await send_msg.send_error("Error: Context Data is Empty")
        else:
            await send_msg.send_response_check_code(response)