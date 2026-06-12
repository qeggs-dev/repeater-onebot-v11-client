from ....assist import PersonaInfo, SendMsg
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import ChangeBranch
from ....clients import ContextClient


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
    cmd_type = CmdTypes.BRANCH_CONTEXT

    def get_client(self, persona_info: PersonaInfo) -> ContextClient:
        return ContextClient(persona_info)