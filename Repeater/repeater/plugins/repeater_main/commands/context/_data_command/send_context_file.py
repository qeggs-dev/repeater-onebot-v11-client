from ....assist import PersonaInfo, SendMsg
from ....cmd_info import CmdTypes
from ....command_register import(
    CommandCaller,
    CommandPackage
)
from ....clients import ContextClient


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
    cmd_type = CmdTypes.CONTEXT

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        user_config = await persona_info.get_user_configs()
        context_client = ContextClient(persona_info, user_config)
        file_url = context_client.get_context_url()
        await send_msg.send_file(file_url, f"{persona_info.namespace_str}_User_Context.json")