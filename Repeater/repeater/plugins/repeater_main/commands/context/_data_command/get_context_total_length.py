from ....assist import PersonaInfo, SendMsg
from ....command_register import(
    CommandCaller,
    CommandPackage,
    CmdType
)
from ..._clients import ContextClient


@CommandCaller.register
class GetContextTotalLength(CommandPackage):
    cmd = "getContextTotalLength"
    aliases = {
        "gctl",
        "GCTL",
        "get_context_total_length",
        "Get_Context_Total_Length",
        "GetContextTotalLength",
        "GET_CONTEXT_TOTAL_LENGTH",
    }
    cmd_type = CmdType.CONTEXT

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        context_client = ContextClient(persona_info)
        response = await context_client.get_context_total_length()

        if response.code == 200:
            data = response.get_data()
            if data is None:
                await send_msg.send_error("Unable to process data.")
            await send_msg.send_prompt(
                f"length: {data.context_length}\n"
                f"total_text_length: {data.total_context_length}\n"
                f"average_content_length: {data.average_content_length}\n"
            )
        else:
            await send_msg.send_response_check_code(response, "Get Context Total Length Failed")