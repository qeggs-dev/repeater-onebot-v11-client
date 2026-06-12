from ....assist import PersonaInfo, SendMsg, CmdTypes
from ....command_register import CommandCaller
from ..._bases import CloneBranchFrom
from ....clients import ContextClient


@CommandCaller.register
class ContextBranchCloneFrom(CloneBranchFrom):
    cmd = "contextBranchCloneFrom"
    aliases = {
        "cbcf",
        "CBCF",
        "context_branch_clone_from",
        "Context_Branch_Clone_From",
        "ContextBranchCloneFrom",
        "CONTEXT_BRANCH_CLONE_FROM",
    }
    cmd_type = CmdTypes.BRANCH_CONTEXT

    def get_client(self, persona_info: PersonaInfo) -> ContextClient:
        return ContextClient(persona_info)