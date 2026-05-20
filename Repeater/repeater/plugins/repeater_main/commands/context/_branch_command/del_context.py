from ....assist import PersonaInfo, SendMsg
from ....command_register import CommandCaller, CmdType
from ..._bases import DeleteBranch
from ..._clients import ContextClient


@CommandCaller.register
class DeleteContext(DeleteBranch):
    cmd = "deleteContext"
    aliases = {
        "dc",
        "DC",
        "delete_context",
        "Delete_Context",
        "DeleteContext",
        "DELETE_CONTEXT",
    }
    cmd_type = CmdType.BRANCH_CONTEXT

    def get_client(self, persona_info: PersonaInfo) -> ContextClient:
        return ContextClient(persona_info)