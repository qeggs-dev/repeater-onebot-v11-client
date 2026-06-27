from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import CloneBranch, UserdataCmdsType

@CommandCaller.register
class ConfigBranchClone(CloneBranch):
    cmd = "configBranchClone"
    aliases = {
        "cfgbc",
        "CFGBC",
        "config_branch_clone",
        "Config_Branch_Clone",
        "ConfigBranchClone",
        "CONFIG_BRANCH_CLONE",
    }
    cmd_type = CmdTypes.BRANCH_CONFIG
    userdata_cmds_type: UserdataCmdsType = UserdataCmdsType.CONFIG