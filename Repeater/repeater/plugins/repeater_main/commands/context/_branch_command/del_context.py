from ....assist import PersonaInfo, SendMsg, CmdTypes
from ....command_register import CommandCaller
from ..._bases import DeleteBranch
from ....clients import ContextClient


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
    cmd_type = CmdTypes.BRANCH_CONTEXT

    def get_client(self, persona_info: PersonaInfo) -> ContextClient:
        return ContextClient(persona_info)