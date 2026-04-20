from ....assist import PersonaInfo, SendMsg
from ....command_register import CommandCaller
from ..._bases import BranchInfo, BranchType
from ..._clients import ContextClient


@CommandCaller.register
class ContextBranchInfo(BranchInfo):
    cmd = "contextBranchInfo"
    aliases = {
        "cbi",
        "CBI",
        "context_branch_info",
        "Context_Branch_Info",
        "ContextBranchInfo",
        "CONTEXT_BRANCH_INFO",
    }
    branch_type = BranchType.Context

    def get_client(self, persona_info: PersonaInfo) -> ContextClient:
        return ContextClient(persona_info)