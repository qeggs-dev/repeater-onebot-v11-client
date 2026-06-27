from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import ChangeBranch, UserdataCmdsType


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
    userdata_cmds_type: UserdataCmdsType = UserdataCmdsType.CONTEXT