from ....assist import PersonaInfo, SendMsg
from ....command_register import CommandCaller
from ..._bases import CloneBranchFrom
from ..._clients import ContextClient


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

    def get_client(self, persona_info: PersonaInfo) -> ContextClient:
        return ContextClient(persona_info)