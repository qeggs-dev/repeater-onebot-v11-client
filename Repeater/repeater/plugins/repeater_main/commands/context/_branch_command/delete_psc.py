from ....assist import PersonaInfo, SendMsg
from ....command_register import CommandCaller, CmdTypes
from ..._bases import DeleteBranch
from ..._clients import ContextClient


@CommandCaller.register
class DeletePublicSpaceContext(DeleteBranch):
    cmd = "deletePublicSpaceContext"
    aliases = {
        "dpsc",
        "DPSC",
        "delete_public_space_context",
        "Delete_Public_Space_Context",
        "DeletePublicSpaceContext",
        "DELETE_PUBLIC_SPACE_CONTEXT",
    }
    cmd_type = CmdTypes.BRANCH_CONTEXT

    def get_client(self, persona_info: PersonaInfo) -> ContextClient:
        return ContextClient(persona_info, namespace=persona_info.public_namespace_str)