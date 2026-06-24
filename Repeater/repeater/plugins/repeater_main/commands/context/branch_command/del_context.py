from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import DeleteBranch, UserdataCmdsType


@CommandCaller.register
class DeleteContext(DeleteBranch):
    cmd = "deleteContext"
    aliases = {
        "dc",
        "DC",
        "delete_context",
        "Delete_Context",
        "DeleteContext",
        "DELETE_CONTEXT",
    }
    cmd_type = CmdTypes.BRANCH_CONTEXT
    userdata_cmds_type: UserdataCmdsType = UserdataCmdsType.CONTEXT