from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BindBranch, UserdataCmdsType


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
    cmd_type = CmdTypes.BRANCH_CONTEXT
    userdata_cmds_type: UserdataCmdsType = UserdataCmdsType.CONTEXT