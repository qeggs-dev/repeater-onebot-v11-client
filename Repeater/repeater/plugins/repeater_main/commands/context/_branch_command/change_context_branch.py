from ....assist import PersonaInfo, SendMsg
from ....command_register import CommandCaller, CmdType
from ..._bases import ChangeBranch
from ..._clients import ContextClient


@CommandCaller.register
class ChangeContextBranch(ChangeBranch):
    cmd = "changeContextBranch"
    aliases = {
        "ccb",
        "CCB",
        "change_context_branch",
        "Change_Context_Branch",
        "ChangeContextBranch",
        "CHANGE_CONTEXT_BRANCH",
    }
    cmd_type = CmdType.BRANCH_CONTEXT

    def get_client(self, persona_info: PersonaInfo) -> ContextClient:
        return ContextClient(persona_info)