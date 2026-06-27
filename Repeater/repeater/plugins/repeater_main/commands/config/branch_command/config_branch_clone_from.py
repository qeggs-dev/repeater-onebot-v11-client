from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import CloneBranchFrom, UserdataCmdsType

@CommandCaller.register
class ConfigBranchCloneFrom(CloneBranchFrom):
    cmd = "configBranchCloneFrom"
    aliases = {
        "cfgbcf",
        "CFGBCF",
        "config_branch_clone_from",
        "Config_Branch_Clone_From",
        "ConfigBranchCloneFrom",
        "CONFIG_BRANCH_CLONE_FROM",
    }
    cmd_type = CmdTypes.BRANCH_CONFIG
    userdata_cmds_type: UserdataCmdsType = UserdataCmdsType.CONFIG