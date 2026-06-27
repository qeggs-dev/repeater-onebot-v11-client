from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import CloneBranch, UserdataCmdsType


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
    cmd_type = CmdTypes.BRANCH_CONTEXT
    userdata_cmds_type: UserdataCmdsType = UserdataCmdsType.CONTEXT