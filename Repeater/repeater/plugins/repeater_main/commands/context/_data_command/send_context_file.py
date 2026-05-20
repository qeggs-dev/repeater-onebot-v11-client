from ....assist import PersonaInfo, SendMsg, FileSender
from ....command_register import(
    CommandCaller,
    CommandPackage,
    CmdType
)
from ..._clients import ContextClient


@CommandCaller.register
class SendContextFile(CommandPackage):
    cmd = "sendContextFile"
    aliases = {
        "scf",
        "SCF",
        "send_context_file",
        "Send_Context_File",
        "SendContextFile",
        "SEND_CONTEXT_FILE",
    }
    type = CmdType.CONTEXT

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        user_file_client = ContextClient(persona_info)
        file_url = user_file_client.get_context_url()
        file_sender = FileSender(
            persona_info=persona_info,
            send_msg=send_msg
        )
        await file_sender.send_file(file_url, f"{persona_info.namespace_str}_User_Context.json")