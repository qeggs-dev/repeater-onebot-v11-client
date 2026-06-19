from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import CloneBranchFrom, UserdataCmdsType


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
    userdata_cmds_type: UserdataCmdsType = UserdataCmdsType.CONTEXT