from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BindBranchFrom, UserdataCmdsType

@CommandCaller.register
class ConfigBranchBindFrom(BindBranchFrom):
    cmd = "configBranchBindFrom"
    aliases = {
        "cfgbbf",
        "CFGBBF",
        "config_branch_bind_from",
        "Config_Branch_Bind_From",
        "ConfigBranchBindFrom",
        "CONFIG_BRANCH_BIND_FROM",
    }
    cmd_type = CmdTypes.BRANCH_CONFIG
    userdata_cmds_type: UserdataCmdsType = UserdataCmdsType.CONFIG