from ....assist import PersonaInfo, SendMsg
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BindBranchFrom
from ....clients import ContextClient


@CommandCaller.register
class ContextBranchBindFrom(BindBranchFrom):
    cmd = "contextBranchBindFrom"
    aliases = {
        "cbbf",
        "CBBF",
        "context_branch_bind_from",
        "Context_Branch_Bind_From",
        "ContextBranchBindFrom",
        "CONTEXT_BRANCH_BIND_FROM",
    }
    cmd_type = CmdTypes.BRANCH_CONTEXT

    def get_client(self, persona_info: PersonaInfo) -> ContextClient:
        return ContextClient(persona_info)