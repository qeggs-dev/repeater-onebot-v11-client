from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import ChangeBranch, UserdataCmdsType, UserdataCmdsType

@CommandCaller.register
class ChangeConfigBranch(ChangeBranch):
    cmd = "changeConfigBranch"
    aliases = {
        "ccfgb",
        "CCFGB",
        "change_config_branch",
        "Change_Config_Branch",
        "ChangeConfigBranch",
        "CHANGE_CONFIG_BRANCH",
    }
    cmd_type = CmdTypes.BRANCH_CONFIG
    userdata_cmds_type: UserdataCmdsType = UserdataCmdsType.CONFIG