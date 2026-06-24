from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BranchInfo, UserdataCmdsType

@CommandCaller.register
class ConfigBranchInfo(BranchInfo):
    cmd = "configBranchInfo"
    aliases = {
        "cfgbi",
        "CFGBI",
        "config_branch_info",
        "Config_Branch_Info",
        "ConfigBranchInfo",
        "CONFIG_BRANCH_INFO",
    }
    cmd_type = CmdTypes.BRANCH_CONFIG
    userdata_cmds_type: UserdataCmdsType = UserdataCmdsType.CONFIG