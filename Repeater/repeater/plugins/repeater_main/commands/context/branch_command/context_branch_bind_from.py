from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BindBranchFrom, UserdataCmdsType


@CommandCaller.register
class ContextBranchBindFrom(BindBranchFrom):
    cmd = "contextBranchBindFrom"
    aliases = {
        "cbbf",
        "CBBF",
        "context_branch_bind_from",
        "Context_Branch_Bind_From",
        "ContextBranchBindFrom",
        "CONTEXT_BRANCH_BIND_FROM",
    }
    cmd_type = CmdTypes.BRANCH_CONTEXT
    userdata_cmds_type: UserdataCmdsType = UserdataCmdsType.CONTEXT