from ....assist import PersonaInfo, SendMsg
from ....command_register import CommandCaller, CmdType
from ..._bases import CloneBranch
from ..._clients import ContextClient


@CommandCaller.register
class ContextBranchClone(CloneBranch):
    cmd = "contextBranchClone"
    aliases = {
        "cbc",
        "CBC",
        "context_branch_clone",
        "Context_Branch_Clone",
        "ContextBranchClone",
        "CONTEXT_BRANCH_CLONE",
    }
    cmd_type = CmdType.BRANCH_CONTEXT

    def get_client(self, persona_info: PersonaInfo) -> ContextClient:
        return ContextClient(persona_info)