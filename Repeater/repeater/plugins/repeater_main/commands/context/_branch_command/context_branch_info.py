from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BranchInfo, UserdataCmdsType


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
    cmd_type = CmdTypes.BRANCH_CONTEXT
    userdata_cmds_type: UserdataCmdsType = UserdataCmdsType.CONTEXT