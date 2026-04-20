from ....assist import PersonaInfo, SendMsg
from ....command_register import CommandCaller
from ..._bases import BindBranch
from ..._clients import ContextClient


@CommandCaller.register
class ContextBranchBind(BindBranch):
    cmd = "contextBranchBind"
    aliases = {
        "cbb",
        "CBB",
        "context_branch_bind",
        "Context_Branch_Bind",
        "ContextBranchBind",
        "CONTEXT_BRANCH_BIND",
    }

    def get_client(self, persona_info: PersonaInfo) -> ContextClient:
        return ContextClient(persona_info)