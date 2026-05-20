from typing import Any
from ...assist import PersonaInfo, SendMsg
from ...command_register import(
    CommandCaller,
    CommandPackage,
    CmdType
)
from .._clients import StatusClient


@CommandCaller.register
class GetCoreTaskStatus(CommandPackage):
    cmd = "getCoreTaskStatus"
    aliases = {
        "gcts",
        "GCTS",
        "get_client_task_status",
        "Get_Client_Task_Status",
        "GetCoreTaskStatus",
        "GET_CORE_TASK_STATUS",
    }
    cmd_type = CmdType.STATUS

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        status_client = StatusClient()
        response = await status_client.get_client_task_status(persona_info.namespace_str)
        if response.code == 200:
            status_stack: list[str] | Any = response.json()
            if not isinstance(status_stack, list):
                await send_msg.send_error("Response data is not a list")
            elif not status_stack:
                await send_msg.send_prompt("Free")
            else:
                text_buffer: list[str] = []
                for index, status in enumerate(status_stack):
                    if index == 0:
                        prefix = ""
                    else:
                        prefix = ("  " * index) + "└ "
                    text_buffer.append(prefix + status)

                await send_msg.send_check_length_prompt("\n".join(text_buffer))
        else:
            await send_msg.send_response_check_code(response)